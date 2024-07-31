from typing import List

settings = {}


class ComponentType: ...


class Queue(metaclass=ComponentType):
    def __init__(self, owner, name, address):
        print(f"Setting {name} for {address}.")

        self.name = owner.name
        self.id = owner.id
        self.active = owner.active
        self.providers = settings.get("providers")
        self.presets = settings.get("presets")

    async def push(self, obj=None):
        await self.queue.lpush(self.name, obj)

    async def pop(self):
        queue, obj = await self.queue.brpop(self.name)
        return await self.process(obj)

    async def process(self, req):
        pass

    async def count(self):
        count = await self.queue.llen(self.name)
        if count == 0:
            pass


def set_queues(address, queues: List[Queue]):
    print(f"Setting queues...")
    for queue in queues:
        instance = Queue(address)
        setattr(queue, instance)
