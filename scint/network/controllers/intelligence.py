from asyncio.subprocess import Process
from enum import Enum
from typing import Any, Dict

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from scint.utils.utils import extract

Preset = Dict[str, Any]
Request = Dict[str, Any]
Response = Dict[str, Any]


class ResponseParser(Process):
    def __init__(self):
        super().__init__()


class RequestBuilder(Process):
    def __init__(self, presets, providers):
        super().__init__()
        self.presets = presets
        self.providers = providers

    async def build_request(self, context):
        pass

    def get_provider(self, provider: str, key: str = None):
        return lambda preset: extract(f"support.{preset}")

    def get_preset(self, preset: str = None, key: str = None):
        return lambda preset: extract(self.presets, preset if preset else "default")

    async def _parse_request(self, composition):
        preset = extract(self.presets, "balanced")
        provider = extract(self.providers, ModelProvider.OPENAI.value)
        paths = provider.get("response_paths")
        method = eval(extract(provider, f"format.{RequestType.TEXT.value}.method"))
        request = await self._create_request(composition, preset)
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
        return {
            **preset,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "response_format": request.response_format,
        }


class Intelligence(Process):
    def __init__(self, providers, presets):
        self.providers = None
        self.requests = RequestBuilder(presets, providers)
        self.responses = ResponseParser()
        super().__init__()

    async def completion(self, req) -> Any:
        req, method, paths = await self._parse_request(req)
        response = await method(**req)
        return dict(**response.choices[0].message.parsed.model_dump())

    async def embedding(self, input: str):
        provider = extract(self.providers, ModelProvider.OPENAI.value)
        method = eval(extract(provider, f"format.{RequestType.EMBEDDING.value}.method"))
        result = await method(model="text-embedding-3-small", input=input)
        return extract(result, "store.0.embedding")

    async def _parse_request(self, req):
        pass


class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class RequestType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    EMBEDDING = "embedding"


class ModelPreset(str, Enum):
    DETERMINISTIC = {
        "model": "gpt-4o-2024-08-06",
        "temperature": 0.4,
        "top_p": 1.2,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
    }
    BALANCED = {
        "model": "gpt-4o-2024-08-06",
        "temperature": 1.4,
        "top_p": 0.6,
        "presence_penalty": 0.25,
        "frequency_penalty": 0.25,
    }
    CREATIVE = {
        "model": "gpt-4o-2024-08-06",
        "temperature": 1.7,
        "top_p": 0.6,
        "presence_penalty": 0.45,
        "frequency_penalty": 0.45,
    }
    IMAGE = {
        "quality": "hd",
        "size": "1024x1024",
        "n": 1,
        "style": "vibrant",
    }
    EMBEDDING = {"model": "text-embeddings-3-small"}


class RequestParams(Process):
    provider = ModelProvider.OPENAI.value
    format = RequestType.TEXT.value
    preset = ModelPreset.BALANCED.value


__all__ = Intelligence, AsyncOpenAI, AsyncAnthropic
