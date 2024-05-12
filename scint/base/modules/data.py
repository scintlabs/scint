import os

from scint.base.modules.components.decorators import metadata
from scint.base.modules.components.module import Module
from scint.base.modules.components.routine import Routine
from scint.support.types import SystemMessage


class FileSystem(Routine):
    """
    The FileSystem Routine is for accessing data and information on the local filesystem.

    Use the functions in this Routine to access data and information on the local filesystem.
    """

    function_choice = {"type": "function", "function": {"name": "list_data"}}

    @metadata(
        description="Use this function to list th contents of a specified path. If no path is provided, the root directory is used.",
        props={
            "path": {
                "type": "string",
                "description": "The directory path to list data from.",
            }
        },
    )
    async def list_data(self, path: str = None):
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


class Data(Module):
    """
    This module provides tools and functions for managing data, including storage, retrieval, and manipulation.

    Use the functions in this module to manage data, including storage, retrieval, and manipulation.
    """

    routines = [FileSystem]
