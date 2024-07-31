from scint.base.models.functions import Function
from scint.base.models.messages import Message
from scint.base.models import Task


class Invoker:
    async def process(self, function: Function):
        await self.queues.invoke.put(function.model_dump_json())

    async def start(self):
        while self.queues.invoke:
            async for res in self.invoke():
                yield res

    async def invoke(self):
        params = await self.queues.invoke.get()
        method = getattr(self, params.pop("method"))

        async for res in await method(params):
            if isinstance(res, Function):
                yield self.queues.invoke.put(res)
            elif isinstance(res, Message):
                yield self.messages.append(res)
            elif isinstance(res, Task):
                yield self.tasks.append(res)

    async def function(self, func, params, callback=None):
        if callback:
            return await func(params.args, callback(params.callback))
        return await func(params.args)

    async def generator(self, params):
        async for res in params.function(params.args):
            yield res

    async def chain(self, params):
        pass
