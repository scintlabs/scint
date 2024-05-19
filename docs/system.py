# import asyncio
# from scint.base.modules.components.decorators import metadata
# from scint.base.modules.components.module import Module
# from scint.base.modules.components.relay import Relay
# from scint.support.logging import log
# from scint.support.types import ContextSnapshot, Message, RouteArguments, SystemMessage
#
#
# class Commands(Relay):
#     """
#     This Routine provides terminal tools and functions for running UNIX terminal commands.
#
#     Use the functions in this Routine to run UNIX terminal commands from a macOS terminal with full sudo privileges.
#     """
#
#     @metadata(
#         description="Use this function to run UNIX terminal commands from a macOS terminal with full sudo privileges.",
#         props={
#             "commands": {
#                 "type": "string",
#                 "description": "The UNIX terminal command to execute.",
#             }
#         },
#     )
#     async def use_terminal(self, commands: str):
#
#         process = await asyncio.create_subprocess_shell(
#             commands,
#             stdout=asyncio.subprocess.PIPE,
#             stderr=asyncio.subprocess.PIPE,
#         )
#
#         stdout, stderr = await process.communicate()
#         output = stdout.decode().strip() if stdout else ""
#         errors = stderr.decode().strip() if stderr else ""
#         full_output = output + "\n" + errors if errors else output
#         yield SystemMessage(content=full_output)
#
#
# class System(Module):
#     """
#     This interface provides system tools and functions for accessing local and remote systems, troubleshooting, and more.
#
#     Use the functions in this module to access system tools and functions for troubleshooting, maintenance, and more.
#     """
#
#     relays = [Commands()]
#     function_choice = {"type": "function", "function": {"name": "route"}}
#
#     async def parse(self, message: Message):
#         log.info(f"{self.name} received message.")
#         self.messages.append(message)
#         async for response in self.intelligence.parse(ContextSnapshot(**self.metadata)):
#             if isinstance(response, RouteArguments):
#                 log.info(f"Routing message {response}.")
#                 res = response.content
#                 relay = res.get("relay")
#                 log.info(f"Relay: {relay}")
#
#                 async for route_res in self.route.call(relay=relay, message=message):
#                     log.info(f"Routing to {relay}.")
#                     yield route_res
#
#             elif isinstance(response, Message):
#                 log.info(f"Returning response.")
#                 yield response
#
#     @metadata(
#         f"Use this function to route messages to the appropriate module.",
#         {
#             "relay": {
#                 "type": "string",
#                 "description": "Select an available relay to process the request.",
#                 "enum": [relay.name for relay in relays],
#             },
#         },
#     )
#     async def route(self, relay: str = None, message=None):
#         if relay:
#             re = next((r for r in System.relays if r.name == relay), None)
#             async for response in re.parse(message):
#                 yield response
