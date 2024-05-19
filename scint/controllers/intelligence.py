import functools
import json

from scint.settings import intelligence
from scint.support.types import Arguments, AssistantMessage, File, Link
from scint.support.types import Any, Dict, List, Optional
from scint.support.types import ContextData
from scint.support.types import Model, ModelParameters, Provider
from scint.support.logging import log


class IntelligenceController:
    def __init__(self):
        self._presets: Dict[str, ModelParameters] = intelligence.get("presets")
        self._providers: Dict[str, Provider] = intelligence.get("providers")

    def _get_provider(self, provider: str, key: Optional[str] = None):
        provider = self._providers.get(provider)
        if key and provider:
            return next((model for model in provider.models if model.name == key), None)
        return provider

    async def process(self, context: ContextData):
        log.info(f"Processing context.")
        preset, method, path = self._parse_context(context)
        request = await self._create_request(context, preset)
        response = await method(**request)
        unpacked_response = await unpack_response(response.model_dump(), path)
        serialized_response = await serialize_response(unpacked_response)
        yield serialized_response

    def _parse_context(self, context: ContextData):
        log.info(f"Parsing context.")
        preset = self._presets.get(context.classification.preset, "balanced")
        provider = self._get_provider(context.classification.provider)
        params = provider.get("format").get(context.classification.format)
        return preset, params.get("method"), params.get("response_path")

    async def _create_request(self, context, preset):
        log.info(f"Creating request from context.")
        messages = []
        for prompt in context.prompts:
            messages.append(prompt.metadata)
        for message in context.messages:
            messages.append(message.metadata)

        request = {
            **preset,
            "messages": messages,
            "tools": [f.metadata for f in context.functions],
        }

        log.info(request)

        return request

    def _load_providers(self, provider_configs: Dict[str, Dict]):
        providers = {}
        for provider_name, provider_config in provider_configs.items():
            models = [
                Model(**model_config) for model_config in provider_config["models"]
            ]
            Provider(**providers[provider_name])
        return providers


async def unpack_response(data: Dict[str, Any], key_paths: List[List[Any]]):
    for path in key_paths:
        attr_path = ".".join(path)

        def rgetattr(obj, attr, *args):
            def _getattr(obj, attr):
                try:
                    if isinstance(obj, dict):
                        return obj[attr]
                    if isinstance(obj, list):
                        return obj[int(attr)]
                    return getattr(obj, attr, *args)
                except (KeyError, IndexError, AttributeError):
                    return None

            return functools.reduce(_getattr, [obj] + attr.split("."))

        response = rgetattr(data, attr_path, None)
        if response is not None:
            return response


async def serialize_response(data: Any):
    log.info(f"Serializing response.")
    if data.get("content") is not None:
        return AssistantMessage(role=data.get("role"), content=data.get("content"))

    if data.get("tool_calls") is not None:
        tool_calls = data.get("tool_calls")
        for tool_call in tool_calls:
            function = tool_call.get("function")
            name = function.get("name")
            args = json.loads(function.get("arguments"))
            return Arguments(name=name, content=args)
    if data.get("url") is not None:
        return Link(data=data.url)
    if data.object.file is not None:
        return File(data=data.file)
    if data.object.embedding is not None:
        return File(data=data.embedding)


intelligence_controller = IntelligenceController()
