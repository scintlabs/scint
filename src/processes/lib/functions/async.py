import asyncio


async def on_request(self, req):
    async def sink(self, req):
        while True:
            try:
                self.queue.append(req)
            except Exception:
                break

    sink_task = asyncio.create_task(self.sink())

    while not sink_task.done():
        while self.running and not self.queue and not sink_task.done():
            await asyncio.sleep(0.1)
        try:
            await self.handler(self.queue.popleft())
        except Exception:
            break

    sink_task.cancel()

    try:
        await sink_task
    except asyncio.CancelledError:
        pass
