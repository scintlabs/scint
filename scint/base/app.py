from scint.base.modules.components.component import ComponentType
from scint.base.modules.components.container import Container
from scint.base.modules.components.decorators import metadata
from scint.base.modules.components.interface import Interface
from scint.base.modules.components.module import Module
from scint.base.modules.data import Data
from scint.base.modules.scheduler import Scheduler
from scint.base.modules.system import System
from scint.support.types import Context, Message, RouteArguments, SystemMessage
from scint.support.types import List
from scint.support.logging import log


class App(metaclass=ComponentType):
    pass


class Scint(App):
    """
    The app component is responsible for coordinating system modules and the interface.

    Route messages to the Interface for general dialogue, Scheduler for events, reminders, and calendars, Data for file system and data parsing operations, and System for command line utilities, logging, and other admin-related tasks.
    """

    interface = Interface()
    modules = [Data(), Scheduler(), System()]
    enum = []
    module_info = []
    for module in modules:
        enum.append(module.name)
        module_info.append(f"{module.name}: {module.description}")

    enum.append(interface.name)
    function_choice = {"type": "function", "function": {"name": "route"}}

    def set_interface(self, interface):
        self.interface = interface

    def set_modules(self, modules: List[Module]):
        if not hasattr(self, "modules"):
            self.modules = []
        for module in modules:
            if isinstance(module, Module):
                self.modules.append(module)

    async def parse(self, message: Message):
        log.info(f"{self.name} received message.")
        self.messages.append(message)
        async for response in self.intelligence.parse(Context(**self.metadata)):
            if isinstance(response, RouteArguments):
                res = response.content
                module = res.get("module")
                note = res.get("note")
                if module == self.interface.name:
                    if note:
                        log.info(f"Sending note to interface.")
                        new = SystemMessage(content=f"{message.content}\n\n{note}")
                        async for note_response in self.interface.parse(new):
                            yield note_response
                    else:
                        log.info(f"Routing message to interface.")
                        async for interface_response in self.interface.parse(message):
                            yield interface_response

                else:

                    async for route_results in self.route.call(module, note, message):
                        yield route_results

            if isinstance(response, Message):
                log.info(f"Sending response to the interface.")
                async for message_response in self.interface.parse(response):
                    yield message_response

    @metadata(
        description=f"This function routes messages to the appropriate module and interface.",
        props={
            "module": {
                "type": "string",
                "description": "Select an available module to process the request.",
                "enum": enum,
            },
            "note": {
                "type": "string",
                "description": "An optional note for the interface.",
            },
        },
    )
    async def route(self, module: str, note: str = None, message=None):
        log.info(f"Looking for {module}.")
        for m in Scint.modules:
            if m.name == module:
                log.info(f"Routing message to {m.name}.")
                async for response in m.parse(message):
                    yield response
