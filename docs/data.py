# import os

# from scint.base.components.decorators import metadata
# from scint.base.components.module import Module
# from scint.base.components.relay import Relay
# from scint.support.logging import log
# from scint.support.types import Context, Message, RouteArguments, SystemMessage


# class FileSystem(Relay):
#     """
#     The FileSystem Routine is for accessing data and information on the local filesystem.

#     Use the functions in this Routine to access data and information on the local filesystem.
#     """

#     function_choice = {"type": "function", "function": {"name": "list_files"}}

#     @metadata(
#         description="Use this function to list th contents of a specified path. If no path is provided, the root directory is used.",
#         props={
#             "path": {
#                 "type": "string",
#                 "description": "The directory path to list data from.",
#             }
#         },
#     )
#     async def list_files(self, path: str = None):
#         base_path = "/Users/kaechle/Developer"
#         data_list = []

#         for item in os.listdir(base_path):
#             item_path = os.path.join(base_path, item)
#             if os.path.isdir(item_path):
#                 data_list.append(f"[DIR] {item}")

#             else:
#                 data_list.append(f"[FILE] {item}")

#         if not data_list:
#             data_list.append("No files or directories found.")

#         list = "\n".join(data_list)
#         log.info(f"List of files and directories: {list}")
#         yield SystemMessage(content=f"The requested data: {list}")


# class Data(Module):
#     """
#     This module provides tools and functions for managing data, including storage, retrieval, and manipulation.

#     You provide tools and functions for managing data, including storage, retrieval, and manipulation.Use the functions in this module to manage data, including storage, retrieval, and manipulation.
#     """

#     modules = []
#     relays = [FileSystem()]
#     function_choice = {"type": "function", "function": {"name": "route"}}

#     async def parse(self, message: Message):
#         log.info(f"{self.name} received message.")
#         self.messages.append(message)
#         async for response in self.intelligence.parse(Context(**self.metadata)):
#             if isinstance(response, RouteArguments):
#                 log.info(f"Routing message {response}.")
#                 res = response.content
#                 relay = res.get("relay")
#                 log.info(f"Relay: {relay}")

#                 async for route_res in self.route.call(relay=relay, message=message):
#                     log.info(f"Routing to {relay}.")
#                     yield route_res

#             elif isinstance(response, Message):
#                 log.info(f"Returning response.")
#                 yield response

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
#             re = next((r for r in self.relays if r.name == relay), None)
#             async for response in re.parse(message):
#                 yield response
