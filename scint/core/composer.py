from scint.core import Core
from scint.core.components import Process
from scint.core.primitives.messages import InputMessage
from scint.core.primitives.instructions import Prompt
from scint.core.primitives.function import Function


class Composer(Core):
    def __init__(self, context, search):
        super().__init__()
        self.context = context
        self.graph = self.context.graph
        self.search = search

    async def compose(self, message: InputMessage):
        last = self.graph.last_active_composition
        last.prompts = await self.compose_prompts("core")
        last.functions = await self.compose_functions(message.sketch)
        reply = await Process(last).evaluate()
        last.messages.append(reply)
        self.graph.sync()
        return reply

    async def compose_prompts(self, args):
        prompts = []
        try:
            results = await self.search("prompts", args)
            for result in results:
                result.pop("id")
                prompts.append(Prompt(**result))
            return prompts
        except Exception as e:
            print(f"Error composing prompts: {e}")

    async def compose_functions(self, query):
        functions = []
        try:
            results = await self.search("functions", query)
            for result in results:
                print(result)
                functions.append(Function(**result))
            return functions
        except Exception as e:
            print(f"Error composing functions: {e}")
