import os

from scint.modules.components.module import Module
from scint.modules.components.scope import Scope
from scint.support.types import Message, SystemMessage
from scint.system.logging import log


class Data(Module):
    """
    This module provides tools and functions for managing data, including storage, retrieval, and manipulation.

    Use the functions in this module to manage data, including storage, retrieval, and manipulation.

    """

    async def select_scope(self, scope_name: str, message: Message):
        description = "This function selects a scope to use."
        props = {
            "scope_name": {
                "type": "string",
                "description": "The scope to switch to.",
                "enum": ["FileSystem"],
            },
        }

        for scope in self.scopes:
            if scope.name == scope_name:
                log.info(f"Forwarding message to {scope}.")
                async for response in scope.parse(message):
                    yield response

            else:
                yield SystemMessage(content=f"Scope {scope_name} not found.")

    class FileSystem(Scope):
        """
        The FileSystem scope is for accessing data and information on the local filesystem.
        Use the functions in this scope to access data and information on the local filesystem.
        """

        async def list_data(self, path: str = None):
            description = "Use this function to list th contents of a specified path. If no path is provided, the root directory is used."
            props = {
                "path": {
                    "type": "string",
                    "description": "The directory path to list data from.",
                }
            }

            base_path = "/Users/kaechle/Developer"
            data_list = []

            for item in os.listdir(base_path):
                item_path = os.path.join(base_path, item)
                if os.path.isdir(item_path):
                    data_list.append(f"[DIR] {item}")

                else:
                    data_list.append(f"[FILE] {item}")

            if not data_list:
                data_list.append("No files or directories found.")

            list = "\n".join(data_list)
            yield SystemMessage(content=f"The requested data: {list}")
