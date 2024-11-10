from scint.ensemble import Search
from scint.ensemble.composer import Composer


class Repository(Composer):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.search = Search()
        self.core = {}

    async def compose(self, message: Message):
        self.messages.append(message)
        self.prompts = await self.compose_prompts()
        self.functions = await self.compose_functions()
        return await self.compose_process(self.core)

    async def compose_process(self, behavior, composition):
        pass

    async def compose_prompts(self):
        prompts = []
        results = await self.search.results("prompts", "framework")
        for result in results:
            result.pop("id")
            prompts.append(Prompt(**result))
        return prompts

    async def compose_functions(self):
        functions = []
        results = await self.search.results("functions", "framework")
        for result in results:
            result.pop("id")
            functions.append(Function(result))
        return functions
