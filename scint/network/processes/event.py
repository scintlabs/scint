import asyncio


class EventProcessor:
    def __init__(self, state_store):
        self.state_store = state_store
        self.processing_queue = asyncio.Queue()

    async def process_event(self, event: dict):
        await self.state_store.update(event["id"])
