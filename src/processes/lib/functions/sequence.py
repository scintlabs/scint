import asyncio


async def start(components):
    for component in components.values():
        if hasattr(component, "start") and callable(component.start):
            await component.start()


async def stop(components, tasks):
    for component in components.values():
        if hasattr(component, "stop") and callable(component.stop):
            await component.stop()
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
