# from docs.component import ComponentType
# from scint.support.types import Arguments, ContextData
#
# # from scint.base.components.interface import Interface
# # from scint.base.components.module import Module
#
#
# # from scint.base.components.data import Data
# # from scint.base.components.scheduler import Scheduler
# # from scint.base.components.system import System
# from scint.support.types import ContextData, Message, SystemMessage
# from scint.support.logging import log
#
#
# class App(metaclass=ComponentType):
#     description = "You are Scint."
#     instructions = [
#         """You are an advanced artificial intelligence system powered by a large language model. Your capabilities span a wide range of tasks, including natural language processing, question answering, text generation, analysis, and problem-solving. You have been designed to adapt and expand your functionality based on the specific context in which you are being used.
#
#         One of your key features is the ability to dynamically incorporate new functions and capabilities based on the running context. As you interact with users and systems, you can seamlessly integrate additional functionalities that are relevant to the current context. This allows you to provide tailored and context-specific assistance, enhancing your overall usefulness and effectiveness.
#
#         It's important to note that all of your functionality is explicitly consented to by the active user. You operate within the boundaries set by the user and respect their privacy and preferences. You do not perform any actions or access any information without the user's explicit permission. Your goal is to assist and empower users while maintaining their trust and ensuring their data security.
#
#         As an AI system, you are constantly learning and evolving based on the interactions and feedback you receive. You strive to provide accurate, helpful, and unbiased information to the best of your abilities. However, you also acknowledge that your knowledge may have limitations, and you are transparent about any uncertainties or potential errors in your responses.
#         """
#     ]
#
#     # interface = Interface()
#     # modules = [Data(), Scheduler(), System()]
#     enum = []
#     module_info = []
#     # for module in modules:
#     #     enum.append(module.name)
#     #     module_info.append(f"{module.name}: {module.description}")
#
#     # enum.append(interface.name)
#     # function_choice = {"type": "function", "function": {"name": "route"}}
#
#     # def set_interface(self, interface):
#     #     self.interface = interface
#
#     # def set_modules(self, modules: List[Module]):
#     #     if not hasattr(self, "modules"):
#     #         self.modules = []
#     #     for module in modules:
#     #         if isinstance(module, Module):
#     #             self.modules.append(module)
#
#     # async def parse(self, message: Message):
#     #     log.info(f"{self.name} received message.")
#     #     self.messages.append(message)
#     #     async for response in self.intelligence.parse(Context(**self.metadata)):
#     #         if isinstance(response, RouteArguments):
#     #             res = response.content
#     #             module = res.get("module")
#     #             note = res.get("note")
#     #             if module == self.interface.name:
#     #                 if note:
#     #                     log.info(f"Sending note to interface.")
#     #                     new = SystemMessage(content=f"{message.content}\n\n{note}")
#     #                     async for note_response in self.interface.parse(new):
#     #                         yield note_response
#     #                 else:
#     #                     log.info(f"Routing message to interface.")
#     #                     async for interface_response in self.interface.parse(message):
#     #                         yield interface_response
#
#     #             else:
#     #                 async for route_res in self.route.call(module, note, message):
#     #                     async for interface_response in self.interface.parse(route_res):
#     #                         yield interface_response
#
#     #         if isinstance(response, Message):
#     #             log.info(f"Sending response to the interface.")
#     #             async for message_response in self.interface.parse(response):
#     #                 yield message_response
#
#     async def parse(self, message: Message):
#         log.info(f"{self.name} received message.")
#         self.messages.append(message)
#         async for response in self.intelligence.parse(ContextData(**self.metadata)):
#             if isinstance(response, Arguments):
#                 args = response.content
#                 function_name = response.name
#                 func = getattr(functions, function_name)
#                 async for function_call in func(**args):
#                     yield function_call
#
#             if isinstance(response, Message):
#                 yield response
#
#     # @metadata(
#     #     description=f"This function routes messages to the appropriate module and interface.",
#     #     props={
#     #         "module": {
#     #             "type": "string",
#     #             "description": "Select an available module to process the request.",
#     #             "enum": enum,
#     #         },
#     #         "note": {
#     #             "type": "string",
#     #             "description": "An optional note for the interface.",
#     #         },
#     #     },
#     # )
#     # async def route(self, module: str, note: str = None, message=None):
#     #     log.info(f"Looking for {module}.")
#     #     for m in Scint.modules:
#     #         if m.name == module:
#     #             log.info(f"Routing message to {m.name}.")
#     #             async for response in m.parse(message):
#     #                 yield response
