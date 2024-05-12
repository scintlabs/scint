import json
from types import FunctionType
from scint.controllers.intelligence import IntelligenceController
from scint.base.modules.components.factory import function_factory
from scint.base.modules.components.container import Container
from scint.base.modules.components.utils import parse_function
from scint.support.types import Arguments, Message, SystemMessage
from scint.support.logging import log


class ComponentType(type):
    intelligence = IntelligenceController

    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return {}

    @classmethod
    async def call_function(cls, arguments: Arguments, message: Message):
        log.info(f"{cls.name} is calling a function.")
        function_name = arguments.content.get("function_name")
        arguments = arguments.content.get("arguments")
        function = cls.route(function_name)
        async for func_res in function.call(arguments, message):
            yield func_res

    @classmethod
    async def use_interface(cls, response: Message):
        log.info(f"{cls.name} is using the interface.")
        async for interface_results in cls.interface.process(response):
            yield interface_results

    def __new__(cls, name, bases, dct, **kwds):
        docstring = dct.get("__doc__", "")
        description, *instructions = docstring.strip().split("\n\n")
        description = SystemMessage(content=description.strip())
        instructions = [SystemMessage(content=item.strip()) for item in instructions]
        container = dct.get("container")
        messages = Container(name)
        function_choice = dct.get("function_choice", "auto")

        def get_metadata(self, dct):
            metadata = {
                "name": name,
                "description": description.metadata,
                "instructions": [i.metadata for i in instructions],
                "function_choice": function_choice,
            }

            for key, value in dct.items():
                if key == "messages":
                    metadata["messages"] = value
                if key == "modules":
                    if not metadata.get("modules"):
                        metadata["modules"] = [module.metadata for module in value]
                if key == "routines":
                    if not metadata.get("routines"):
                        metadata["routines"] = [routine.metadata for routine in value]
                if hasattr(value, "props"):
                    if not metadata.get("functions"):
                        metadata["functions"] = []
                    metadata["functions"].append(value.metadata)
                if isinstance(value, FunctionType) and parse_function(value):
                    if not metadata.get("functions"):
                        metadata["functions"] = []
                    function = function_factory(value)
                    metadata["functions"].append(function.metadata)
                if key == "function_choice":
                    metadata["function_choice"] = value

            self.metadata = metadata
            return self.metadata

        dct["name"] = name
        dct["description"] = description
        dct["instructions"] = instructions
        dct["messages"] = messages
        dct["function_choice"] = function_choice
        dct["container"] = container
        dct["metadata"] = get_metadata(cls, dct)
        dct["call_function"] = cls.call_function
        dct["use_interface"] = cls.use_interface
        dct["intelligence"] = IntelligenceController()
        return super().__new__(cls, name, bases, dct, **kwds)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance
