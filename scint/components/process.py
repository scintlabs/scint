import uuid
from inspect import getclasstree
from typing import Self

import injector

from scint.components.config import Preset
from scint.components.core import CoreModule, ICoreProvider
from scint.components.models import Message, SystemMessage
from scint.utils.logger import log


class ProcessMeta(type):
    injector_instance = injector.Injector([CoreModule()])
    core_provider = injector_instance.get(ICoreProvider)

    def __new__(mcls, name, bases, dct, *args, **kwargs):
        cls = super().__new__(mcls, name, bases, dct)
        dct["name"] = name
        dct["id"] = uuid.uuid4()
        dct["execution_map"] = dct.get("build_execution_map")
        dct["classref"] = cls

        ProcessMeta.core_provider.register(
            name=name,
            id=str(dct.get("id")),
            preset=dct.get("preset"),
            description=dct.get("description", "You are a friendly assistant."),
            tooling=dct.get("tooling", []),
            classref=cls,
        )
        return cls

    def __init__(cls, name, bases, dct):
        cls.name = name
        cls.core = ProcessMeta.core_provider
        cls.generate_tool_call = cls.core.generate_tool_call
        super().__init__(name, bases, dct)


class Process(metaclass=ProcessMeta):
    preset = Preset.process
    description = "You are a nifty process."
    tooling = []
    subprocesses = []

    def build_execution_map(self):
        execution_map = self._recurse_subprocesses()
        return execution_map

    def _recurse_subprocesses(self):
        core = self.core.get_process_state(self.name)

        process_map = {
            self.name: {
                "Tools": [tool.name for tool in core.tools.tools],
            }
        }

        for subprocess in self.subprocesses:
            subprocess_map = subprocess._recurse_subprocesses()
            process_map[self.name].update(subprocess_map)

        return process_map

    def build_execution_list(self, execution_map, execution_list):
        for key, value in execution_map.items():
            if key != "Tools":
                execution_list.append(key)

            if isinstance(value, dict):
                self.build_execution_list(value, execution_list)

        return execution_list

    async def execute(self, message):
        execution_list = []
        responses = []
        execution_map = self.build_execution_map()
        process_list = self.build_execution_list(execution_map, execution_list)
        log.info(process_list)
        while process_list:
            process_name = process_list.pop() if process_list else None
            # if process_name == "Main":
            #     process_name = process_list.pop()

            process = self.core.get_process_instance(process_name)
            message.sender = process_name
            message.receiver = process.name
            async for response in self.subprocess_tool_call(process, message):
                responses.append(response)
                yield response

        if responses:
            yield responses[-1]

    async def subprocess_tool_call(self, process, message):
        async for response in process.generate_tool_call(message):
            yield response
