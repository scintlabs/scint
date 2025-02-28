from anthropic import AsyncAnthropic
from openai import AsyncOpenAI, OpenAI

from src.types.signals import Message
from src.types import Struct, Trait


class Configuration(Struct): ...


class Providers(Struct):
    openai_sync: OpenAI = OpenAI()
    openai: AsyncOpenAI = AsyncOpenAI()
    anthropic: AsyncAnthropic = AsyncAnthropic()


class Intelligent(Trait):
    def configure(self):
        return {"model": "gpt-4o", "temperature": 1.4, "top_p": 0.6, **self.model}

    async def think(self):
        cfg = self.configure()
        cfg["response_format"] = Message
        res = await Providers.openai.beta.chat.completions.parse(**cfg)
        msg = res.choices[0].message
        self.state.update(msg.parsed)
        if msg.tool_calls is not None:
            return await self.process(msg.tool_calls)
        return

    async def process(self, tool_calls):
        for call in tool_calls:
            tool = self._tools.get(call.function.name, None)
            if tool is not None:
                res = await tool(call)
                self.state.update(res)
                return await self.think()
            return

    async def reason(self):
        pass

    def classify(input: str):
        req = {"model": "text-embedding-3-small", "input": str(input)}
        return Providers.openai_sync.embeddings.create(**req).data[0].embedding
