# from scint.base.components.component import ComponentType
# from scint.base.components.relay import Relay
# from scint.support.types import Context, Message, RouteArguments
# from scint.support.types import List
# from scint.support.logging import log


# class Module(metaclass=ComponentType):
#     modules = []
#     relays = []
#     module_info = []

#     for module in modules:
#         module_info.append(f"{module.name}: {module.description}")

#     for relay in relays:
#         module_info.append(f"{relay.name}: {relay.description}")

#     function_choice = {"type": "function", "function": {"name": "route"}}

#     def set_modules(self, modules: List["Module"]):
#         for module in modules:
#             if isinstance(module, Module):
#                 self.modules.append(module)

#     def set_relays(self, relays: List[Relay]):
#         for relay in relays:
#             if isinstance(relay, Relay):
#                 self.modules.append(relay)

#     async def parse(self, message: Message):
#         log.info(f"{self.name} received message.")
#         self.messages.append(message)
#         async for response in self.intelligence.parse(Context(**self.metadata)):
#             if isinstance(response, RouteArguments):
#                 log.info(f"Routing message {response}.")
#                 res = response.content
#                 module = res.get("module")
#                 log.info(f"Module: {module}")
#                 relay = res.get("relay")
#                 log.info(f"Relay: {relay}")
#                 if module:
#                     async for route_res in self.route.call(
#                         module=module, message=message
#                     ):
#                         log.info(f"Routing to {module}.")
#                         yield route_res
#                 elif relay:
#                     async for route_res in self.route.call(
#                         relay=relay, message=message
#                     ):
#                         log.info(f"Routing to {relay}.")
#                         yield route_res

#             elif isinstance(response, Message):
#                 log.info(f"Returning response.")
#                 yield response

#     # @metadata(
#     #     f"Use this function to route messages to the appropriate module.",
#     #     {
#     #         "relay": {
#     #             "type": "string",
#     #             "description": "Select an available relay to process the request.",
#     #             "enum": [relay.name for relay in relays],
#     #         },
#     #         "module": {
#     #             "type": "string",
#     #             "description": "Select an available module to process the request.",
#     #             "enum": [module.name for module in modules],
#     #         },
#     #     },
#     # )
#     # async def route(self, module: str = None, relay: str = None, message=None):
#     #     if relay:
#     #         re = getattr(self, relay)
#     #         async for response in re.parse(message):
#     #             yield response
#     #     elif module:
#     #         mo = getattr(self, module)
#     #         async for response in mo.parse(message):
#     #             yield response
