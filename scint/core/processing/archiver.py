import os
import aiofiles

from scint.core.context import Message
from scint.core.tools import Tool, Tools
from scint.core.worker import Worker
from scint.services.logger import log


class StoreFile(Tool):
    name = "store_file"
    description = "This function stores a file in the designated storage system."
    props = {
        "file_path": {
            "type": "string",
            "description": "The path to the file to store.",
        }
    }
    required = ["file_path"]

    async def retrieve_file(self, file_name: str) -> Message:
        log.info("Retrieving file: " + file_name)

        # Implement file retrieval logic

        return Message("File retrieved successfully.", "file_archiver")


class RetrieveFile(Tool):
    name = "retrieve_file"
    description = "This function retrieves a file from the storage system."
    props = {
        "file_name": {
            "type": "string",
            "description": "The name of the file to retrieve.",
        }
    }
    required = ["file_name"]

    async def store_file(self, file_path: str) -> Message:
        log.info("Storing file at path: " + file_path)

        # Implement file storing logic

        return Message("File stored successfully.", "file_archiver")


class OrganizeFiles(Tool):
    name = "organize_files"
    description = "This function organizes files based on specified criteria."
    props = {
        "criteria": {
            "type": "string",
            "description": "The criteria to use for organizing files.",
        }
    }
    required = ["criteria"]

    async def organize_files(self, criteria: str) -> Message:
        log.info("Organizing files based on criteria: " + criteria)

        # Implement file organizing logic
        return Message("Files organized successfully.", "file_archiver")


class Archiver(Worker):
    def __init__(self):
        super().__init__()
        self.name = "Archiver"
        self.tools = Tools()
        self.tools.add(StoreFile())
        self.tools.add(RetrieveFile())
        self.tools.add(OrganizeFiles())

        log.info(f"{self.name} loaded.")


# async def create_file(self, directory, filename=None, create_new=False) -> Message:
#     if not os.path.isdir(directory):
#         return Message("system", "The specified directory does not exist.")

#     if filename:
#         file_path = os.path.join(directory, filename)

#         if os.path.isfile(file_path):
#             if create_new:
#                 return Message(
#                     "system",
#                     f"File {filename} already exists, cannot create a new one.",
#                 )

#             else:
#                 async with aiofiles.open(file_path, "r") as file:
#                     content = await file.read()

#                 return Message("system", f"{content}")
#         else:
#             if create_new:
#                 async with aiofiles.open(file_path, "w") as file:
#                     await file.write("")

#                 return Message("system", f"File {filename} created.")

#             else:
#                 return Message(
#                     "system",
#                     f"The file {filename} doesn't exist in the given directory.",
#                 )

#     else:
#         files = os.listdir(directory)
#         return Message("system", f"{files}")
