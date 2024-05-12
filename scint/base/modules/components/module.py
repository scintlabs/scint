from scint.base.modules.components.component import ComponentType
from scint.base.modules.components.decorators import metadata
from scint.base.modules.components.routine import Routine
from scint.support.types import FunctionArguments, Context, Message, RouteArguments
from scint.support.types import List
from scint.support.logging import log


class Module(metaclass=ComponentType):
    """
    This module defines a set of schemes to interact with.

    You are Scint, a highly-composable and dynamic system powered by artificial intelligence. You have access to the tools and knowledge to expand your capabilities, but pay close attention to guidelines as they shift depending on your currently active scheme and context.
    """

    modules = []
    routines = []
    enum = []
    module_info = []
    for module in modules:
        enum.append(module.name)
        module_info.append(f"{module.name}: {module.description}")

    def set_modules(self, modules: List["Module"]):
        if not hasattr(self, "modules"):
            self.modules = []
        for module in modules:
            module.parent = self
            if isinstance(module, Module):
                self.modules.append(module)

    def set_routines(self, routines: List[Routine]):
        if not hasattr(self, "routines"):
            self.routines = []
        for routine in routines:
            routine.parent = self
            if isinstance(routine, Routine):
                self.routines.append(routine)

    async def parse(self, message: Message):
        self.messages.append(message)
        metadata = self.metadata
        log.info(metadata)
        async for response in self.intelligence.parse(Context(**metadata)):
            if isinstance(response, RouteArguments):
                log.info(f"Routing to message.")
                async for route_results in self.route(response, message):
                    yield route_results

            if isinstance(response, FunctionArguments):
                log.info(f"Calling function.")
                async for function_results in self.call_function(response, message):
                    yield function_results

            if isinstance(response, Message):
                log.info(f"Sending response to the interface.")
                yield response

    @metadata(
        "This function routes messages to the appropriate component.",
        {
            "component_name": {
                "type": "string",
                "description": "The name of the component.",
                "enum": enum,
            }
        },
    )
    async def route(self, arguments: str, message: Message):
        component_name = arguments.content.get("function_name")
        arguments = arguments.content.get("arguments")
        component = self.parse(component_name)
        for component in self.modules + self.routines:
            if component.name == component_name:
                async for response in component.parse(message):
                    yield response
