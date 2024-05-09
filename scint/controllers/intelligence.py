import functools
import json

from scint.system.configure import intelligence
from scint.support.types import Arguments, File, Link, Any, Dict, List, Optional
from scint.support.types import Context, Message
from scint.support.types import Model, ModelParameters, Provider
from scint.system.logging import log


class IntelligenceController:
    def __init__(self):
        self._presets: Dict[str, ModelParameters] = intelligence.get("presets")
        self._providers: Dict[str, Provider] = intelligence.get("providers")

    async def parse(self, context: Context):
        parsed_context, method, path = self._parse_context(context)
        request = self._create_request(parsed_context)
        response = await method(**request)
        unpacked_response = await unpack_response(response.model_dump(), path)
        serialized_response = await serialize_response(unpacked_response)
        yield serialized_response

    def _parse_context(self, context: Context):
        parsed_context = context
        parsed_context.preset = self._presets.get(context.preset, "balanced")
        provider = self._get_provider(context.classification.provider)
        params = provider.get("format").get(context.classification.format)
        return parsed_context, params.get("method"), params.get("response_path")

    def _create_request(self, context):
        request = {
            **context.preset,
            "messages": [message.get_metadata() for message in context.messages],
        }

        if len(context.functions) > 0:
            request["tools"] = []
            for function in context.functions:
                function = {"type": "function", "function": function.model_dump()}
                request["tools"].append(function)

            if context.function_choice:
                request["tool_choice"] = context.function_choice

        return request

    def _get_provider(self, provider: str, key: Optional[str] = None):
        provider = self._providers.get(provider)
        if key and provider:
            return next((model for model in provider.models if model.name == key), None)

        return provider

    def _load_providers(self, provider_configs: Dict[str, Dict]):
        providers = {}
        for provider_name, provider_config in provider_configs.items():
            models = [
                Model(**model_config) for model_config in provider_config["models"]
            ]
            providers[provider_name] = Provider(
                name=provider_name, module=None, models=models
            )
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
    if data.get("content") is not None:
        return Message(role=data.get("role"), content=data.get("content"))

    if data.get("tool_calls") is not None:
        tool_calls = data.get("tool_calls")
        for tool_call in tool_calls:
            function = tool_call.get("function")
            name = function.get("name")
            args = function.get("arguments")
            return Arguments(name=name, content=json.loads(args))

    if data.get("url") is not None:
        return Link(url=data.url)
    if data.object.file is not None:
        return File(data=data.file, type="file")
    if data.object.embedding is not None:
        return File(data=data.embedding, type="embedding")
