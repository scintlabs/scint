from deltron.data.pipeline import Message, SearchMessage, SystemMessage


async def keyword_search(message):
    pass


async def semantic_search(message):
    pass


class Search:
    async def keywords(self, message):
        async for keyword_match in keyword_search(message):
            yield keyword_match

    async def semantic(self, message):
        async for semantic_match in semantic_search(message):
            yield semantic_match

    async def merged(self, message: SearchMessage):
        async for keyword_match in self.keywords(message):
            yield keyword_match

        async for semantic_match in self.semantic(message):
            yield semantic_match
