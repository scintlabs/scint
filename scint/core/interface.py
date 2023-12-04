import asyncio

from scint.core.persona import Persona
from scint.core.coordinator import Coordinator
from scint.services.logger import log


class ScintInterface:
    def __init__(self) -> None:
        self.persona = Persona()
        self.coordinator = Coordinator()

    async def chat(self, request):
        tasks = [
            asyncio.create_task(
                self._process_generator(self.persona.process_request(request))
            ),
            asyncio.create_task(
                self._process_generator(self.coordinator.process_request(request))
            ),
        ]

        while tasks:
            done, pending = await asyncio.wait(
                tasks, return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                message = task.result()
                if message is not None:
                    yield message

            tasks = list(pending)

    async def _process_generator(self, async_gen):
        try:
            return await async_gen.__anext__()
        except StopAsyncIteration:
            return None
