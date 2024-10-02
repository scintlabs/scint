from typing import List, Dict, Any
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from scint.framework.models import OutputMessage
from scint.framework.models import RequestType, Provider
from scint.framework.entities.service import Service
from scint.framework.utils.serialize import dictorial


__all__ = "AsyncOpenAI", "AsyncAnthropic"

Preset = Dict[str, Any]
CompletionRequest = Dict[str, Any]
Embedding = List[float]


class Intelligence(Service):
    def __init__(self, context, presets, providers):
        super().__init__()
        self.providers = providers
        self.presets = presets
        context.get_preset = self.get_preset
        context.get_provider = self.get_provider
        context.process = self.process
        context.embedding = self.embedding

    def get_preset(self, preset: str) -> Preset:
        return lambda preset: dictorial(self.presets, preset)

    def get_provider(self, provider: str, key: str = None):
        return lambda p: dictorial(f"support.{p}")

    async def process(self, composition) -> Any:
        request, method, paths = await self._parse_composition(composition)
        response = await method(**request)
        message = OutputMessage(**response.choices[0].message.parsed.model_dump())
        return message

    async def _parse_composition(self, composition):
        preset = dictorial(self.presets, "balanced")
        provider = dictorial(self.providers, Provider.OPENAI.value)
        method = eval(
            dictorial(provider, f"format.{RequestType.COMPLETION.value}.method")
        )
        request = await self._create_request(composition, preset)
        paths = provider.get("response_paths")
        return request, method, paths

    async def _create_request(self, request, preset: Preset):
        messages = []
        tools = []
        for prompt in request.prompts:
            messages.append(prompt.index)
        for message in request.messages:
            messages.append(message.index)
        for function in request.functions:
            tools.append(function.index)
        req = {
            **preset,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "response_format": request.response_format,
        }
        return req

    async def embedding(self, input_value: str) -> Embedding:
        provider = dictorial(self.providers, Provider.OPENAI.value)
        method = eval(
            dictorial(provider, f"format.{RequestType.EMBEDDING.value}.method")
        )
        result = await method(model="text-embedding-3-small", input=input_value)
        return dictorial(result, "store.0.embedding")
