from __future__ import annotations

import json

from src.core.types.signals import Output, ToolCall
from src.core.types.identity import protocol
from src.core.util.llms import build_request, oai
from src.core.util.tooling import tool
from src.lib.instructions import interface, executor, composer
from src.lib.tools import use_terminal


@protocol
class Agent:
    Analysis = (composer, Output, [use_terminal])
    Hypothesis = (composer, Output, [use_terminal])
    Execution = (executor, Output, [use_terminal])
    Dialogue = (interface, Output, [use_terminal])

    def __init__(self, proto):
        instr, out, tools = proto
        self.instructions = instr
        self.output = out
        self.tools = [tool(t) for t in tools]

    def __call__(self, *args):
        return build_request(self, args)

    async def parse(self, req):
        res = await oai.responses.create(**req)
        for obj in res.output:
            if obj.type == "message":
                for content in obj.content:
                    output = Output(**json.loads(content.text))
                    yield output
            if obj.type == "function_call":
                async for r in self.execute(obj):
                    yield r

    async def execute(self, call: ToolCall):
        tool_call = ToolCall(call.call_id, call.name, call.arguments)
        for t in self.tools:
            if tool_call.name == t.name:
                args = json.loads(tool_call.arguments)
                res = await t.function(**args)
                res.id = tool_call.id
                async for res in self.parse():
                    yield res
