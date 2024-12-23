import asyncio
from typing import List
from ..processes.types import Process, ProcessType


class Processor(metaclass=ProcessType):
    def __init__(self, *args, **kwargs):
        self.processes: List[Process] = []

    async def start(self, components):
        for component in components.values():
            if hasattr(component, "start") and callable(component.start):
                await component.start()

    async def stop(self, components, tasks):
        for component in components.values():
            if hasattr(component, "stop") and callable(component.stop):
                await component.stop()
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


load_process = {
    "type": "function",
    "function": {
        "name": "load_process",
        "description": "Load a process, workflow, or sequence and pass it to the Processor to accomplish a specific, multi-step task. Use this function when the user needs to accomplish a task that matches one of the processes listed.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the process to load.",
                    "enum": [],
                },
            },
            "required": ["name"],
            "additionalProperties": False,
        },
    },
}
