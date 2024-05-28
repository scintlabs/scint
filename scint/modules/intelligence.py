from scint.settings import intelligence
from scint.core.models import Completion
from scint.support.types import Dict, Optional
from scint.support.types import Model, ModelParameters, Provider
from scint.modules.logging import log
from scint.support.utils import serialize_response


class IntelligenceController:
    def __init__(self):
        self._presets: Dict[str, ModelParameters] = intelligence.get("presets")
        self._providers: Dict[str, Provider] = intelligence.get("providers")

    async def process(self, request: Completion):
        log.info(f"Processing request.")
        try:
            req, method, paths = await self._parse_request(request)
            if req is None or method is None or paths is None:
                log.error("Failed to parse request.")
                return
            result = await method(**req)
            response = await serialize_response(result.model_dump(), paths)
            log.info(response)
            yield response
        except Exception as e:
            log.error(f"Error processing request: {e}")

    async def _parse_request(self, request: Completion):
        log.info(f"Parsing request.")
        try:
            preset = self._presets.get(request.classification.preset)
            provider = self._get_provider(request.classification.provider)
            params = provider.get("format").get(request.classification.format)
            new_request = await self._create_request(request, preset)
            return new_request, params.get("method"), provider.get("response_paths")
        except Exception as e:
            log.error(f"Error parsing request: {e}")
            return None, None, None

    async def _create_request(self, context, preset):
        log.info(f"Creating request from context.")
        try:
            request = {**preset, "messages": [], "tools": []}
            for prompt in context.prompts:
                request["messages"].append(prompt.metadata)
            for message in context.messages:
                request["messages"].append(message.metadata)
            for function in context.functions:
                request["tools"].append(function.metadata)
            return request
        except Exception as e:
            log.error(f"Error creating request: {e}")
            return None

    def _load_providers(self, cfgs: Dict[str, Dict]):
        log.info(f"Loading providers.")
        providers = {}
        for provider_name, provider_config in cfgs.items():
            models = [Model(**cfg) for cfg in provider_config["models"]]
            providers[provider_name] = Provider(name=provider_name, models=models)
        return providers

    def _get_provider(self, provider: str, key: Optional[str] = None):
        log.info(f"Getting provider.")
        provider = self._providers.get(provider)
        if key and provider:
            return next((model for model in provider.models if model.name == key), None)
        return provider


intelligence_controller = IntelligenceController()
