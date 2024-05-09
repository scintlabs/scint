import types

from scint.controllers.intelligence import IntelligenceController
from scint.modules.components.callable import function_factory
from scint.modules.components.container import Container
from scint.modules.components.scope import ScopeType
from scint.support.types import Arguments, Context, Message, SystemMessage
from scint.system.logging import log


class ModuleType(type):
    intelligence = IntelligenceController

    @classmethod
    def __prepare__(dct, *args, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, *args, **kwargs):
        name = name
        functions = []
        function_choice = {"type": "function", "function": {"name": "select_scope"}}
        function_choice = "auto"
        modules = []
        module_choice = {}
        scopes = []
        scope_choice = {}
        docstring = dct.get("__doc__", "")
        description, *instructions = docstring.strip().split("\n\n")
        instructions = [SystemMessage(content=item.strip()) for item in instructions]

        for attr_name, attr_value in dct.items():
            if isinstance(attr_value, types.FunctionType):
                functions.append(function_factory(attr_value))
            if isinstance(attr_value, ModuleType):
                modules.append(attr_value())
            if isinstance(attr_value, ScopeType):
                scopes.append(attr_value())

        async def parse(self, message: Message):
            log.info(f"{self.name} is parsing a message: {message}")
            self.messages.append(message)
            metadata = self.get_metadata()
            async for response in self.intelligence.parse(Context(**metadata)):
                if isinstance(response, Arguments):
                    comp_name = response.content.get("component_name")
                    async for func_res in self.select_component(comp_name, message):
                        self.messages.append(func_res)
                        yield func_res

                if isinstance(response, Message):
                    yield response

        def get_metadata(self):
            log.info(f"{self.name} is retrieving metadata.")

            metadata = {
                "name": self.name,
                "description": self.description,
                "instructions": [item.get_metadata() for item in self.instructions],
                "messages": [message.get_metadata() for message in self.messages],
                "functions": [func.get_metadata() for func in self.functions],
                "function_choice": self.function_choice,
                "modules": [module.get_metadata() for module in self.modules],
                "module_choice": self.module_choice,
                "scopes": [scope.get_metadata() for scope in self.scopes],
                "scope_choice": self.scope_choice,
            }

            log.info(metadata)
            return metadata

        dct["name"] = name
        dct["description"] = description
        dct["instructions"] = instructions
        dct["messages"] = Container(name)
        dct["functions"] = functions
        dct["function_choice"] = function_choice
        dct["modules"] = modules
        dct["module_choice"] = module_choice
        dct["scopes"] = scopes
        dct["scope_choice"] = scope_choice
        dct["parse"] = parse
        dct["get_metadata"] = get_metadata
        dct["intelligence"] = IntelligenceController()

        return super().__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name, bases, dct):
        return type.__init__(cls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class Module(metaclass=ModuleType):
    """
    This module defines a set of schemes to interact with.

    You are Scint, a highly-composable and dynamic system powered by artificial intelligence. You have access to the tools and knowledge to expand your capabilities, but pay close attention to guidelines as they shift depending on your currently active scheme and context.
    """
