from scint.base.models.functions import Function
from scint.base.models.messages import Prompt


class ComposerType(type):
    _prototype = None

    @classmethod
    def __prepare__(cls, name, bases, *args, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class Composer(metaclass=ComposerType):
    def __init__(self):
        super().__init__()

    async def compose(self, actor):
        query = await self._build_query(actor)
        await self._get_prompts(actor, query)
        await self._get_functions(actor, query)

    async def build_query(self, actor):
        query = ""
        for message in actor.messages.messages:
            for String in message.data:
                query += String.data
        return query

    async def get_prompts(self, actor, query):
        categories = ["identity", "instructions"]
        for category in categories:
            prompt = await self.search.results("prompts", query, category, 1)
            setattr(actor, category, Prompt(**prompt[0]))

    async def get_functions(self, actor, query):
        category = "core"
        results = await self.search.results("functions", query, category, 5)
        for result in results:
            actor.functions.append(Function(**result))
