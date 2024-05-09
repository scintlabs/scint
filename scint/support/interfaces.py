from scint.support.types import AsyncGenerator


class IEvent: ...


class IStorage: ...


class ISearch: ...


class IIntelligence:
    async def parse(self, snapshot):
        pass


class IContext:
    def container(self, name):
        pass
