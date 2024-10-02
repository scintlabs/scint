from scint.framework import Construct, Message, Instruction, Process
from scint.framework import Function


class Invoker(Construct):
    def __init__(self):
        super().__init__()
        self.process = Process()

    async def process(self, function: Function):
        await self.queues.invoke.put(function.model_dump_json())

    async def start(self):
        while self.queues.invoke:
            await self.invoke()

    async def invoke(self):
        params = await self.queues.invoke.get()
        method = getattr(self, params.pop("method"))

        async for res in await method(params):
            if isinstance(res, Function):
                yield self.queues.invoke.put(res)
            elif isinstance(res, Message):
                yield self.messages.append(res)
            elif isinstance(res, Instruction):
                yield self.tasks.append(res)

    async def function(self, func, params, callback=None):
        if callback:
            return await func(params.args, callback(params.callback))
        return await func(params.args)
