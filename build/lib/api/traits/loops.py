import asyncio

from scint.api.types import Trait


class Loop(Trait):
    async def process(self, handler: Trait):
        async def sink():
            while True:
                try:
                    sig = await self.tasks.enque.get()
                    await self.handle(sig)
                except Exception as e:
                    print(f"Error processing signal: {e}")

        sink_task = asyncio.create_task(sink())

        while not sink_task.done():
            try:
                res = await self.tasks.deque.get()
                if res:
                    self.output(res)
            except Exception as e:
                print(f"Error processing signal: {e}")

        sink_task.cancel()
        try:
            await sink_task
        except asyncio.CancelledError:
            pass
