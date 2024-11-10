import asyncio


class Control: ...


class Start(Control):
    async def start(components):
        for component in components.values():
            if hasattr(component, "start") and callable(component.start):
                await component.start()

    def values(self):
        pass


class Stop(Control):
    async def stop(components, tasks):
        for component in components.values():
            if hasattr(component, "stop") and callable(component.stop):
                await component.stop()
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    def values(self):
        pass


class Fork(Control):
    async def call(self, *args, **kwargs):
        pass
