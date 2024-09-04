from enum import Enum
from typing import List, Optional

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from pydantic import BaseModel

from scint.services import Service
from scint.core.utils.dicts import dictorial
from scint.core.utils.serialize import unpack_response


__all__ = "AsyncOpenAI", "AsyncAnthropic", "Intelligence", "ProviderParameters"


class BlockType(str, Enum):
    text = "text"
    code = "code"
    link = "link"


class Block(BaseModel):
    type: BlockType
    data: str


class MessageFormat(BaseModel):
    blocks: List[Block]
    semantic_labels: List[str]
    annotation: str


class Intelligence(Service):
    def __init__(self, context, providers, presets):
        self.providers = providers
        self.presets = presets
        self.context = context.create("intelligence")
        self.context.get_preset = self.get_preset
        self.context.get_provider = self.get_provider
        self.context.process = self.process
        self.context.embedding = self.embedding

    def get_preset(self, preset):
        return lambda preset: dictorial(self._presets, preset)

    def get_provider(self, provider: str, key: Optional[str] = None):
        return lambda p: dictorial(f"support.{p}")

    async def process(self, composition):
        try:
            req, method, paths = await self.parse_request(composition)
            res = await method(**req)
            print(res)
            return await unpack_response(res, paths)
        except Exception as e:
            print(f"Error processing intelligence request: {e}")

    async def parse_request(self, request):
        try:
            preset = dictorial(self.presets, "balanced")
            provider = dictorial(self.providers, "openai")
            method = dictorial(provider, "format.completion.method")
            meth = eval(method)
            req = await self.create_request(request, preset)
            print(req)
            paths = provider.get("response_paths")
            return req, meth, paths
        except Exception as e:
            print(f"Error parsing intelligence request: {e}")

    async def create_request(self, request, preset):
        try:
            response_format = MessageFormat
            messages = []
            for p in request.prompts:
                messages.append(p.index)
            for m in request.messages:
                messages.append(m.index)
            req = {**preset, "messages": messages, "response_format": response_format}
            if request.functions:
                tools = []
                for f in request.functions:
                    tools.append(f.index)
                req["tools"] = tools
                req["tool_choice"] = "auto"
            return req
        except Exception as e:
            print(f"Error creating intelligence request: {e}")

    async def embedding(self, input_value: str):
        try:
            provider = dictorial(self.providers, "openai")
            method = eval(dictorial(provider, "format.embedding.method"))
            result = await method(model="text-embedding-3-small", input=input_value)
            return dictorial(result, "store.0.embedding")
        except Exception as e:
            print(f"Error generating embedding: {e}")

    async def interpret(self, composition):
        try:
            provider = dictorial(self.providers, "openai")
            method = eval(dictorial(provider, "format.completion.method"))
            result = await method(messages=composition.messages, model="gpt-4o")
            return dictorial(result, "choices.0.message.content")
        except Exception as e:
            print(f"Error generating completion: {e}")


class ProviderParameters(BaseModel):
    provider: str = "openai"
    format: str = "completion"
    preset: str = "balanced"
