from scint.core.processes import Process
from scint.core.messages import SystemMessage
from scint.core.tools import Tool, Tools
from scint.services.logger import log


class FileRead(Tool):
    name = "file_read"
    description = "Reads content from a specified file."
    props = {
        "file_path": {
            "type": "string",
            "description": "The path to the file to be read.",
        },
    }
    required = ["file_path"]

    async def execute_action(self, file_path: str) -> SystemMessage:
        try:
            with open(file_path, "r") as file:
                file_content = file.read()

            return SystemMessage(file_content, self.__class__.__name__)

        except Exception as e:
            log.error(f"Error reading file: {e}")
            return SystemMessage(f"Unable to read file.", self.__class__.__name__)


class FileWrite(Tool):
    name = "file_write"
    description = "Writes content to a specified file."
    props = {
        "file_path": {
            "type": "string",
            "description": "The path to the file to be written to.",
        },
        "content": {
            "type": "string",
            "description": "The content to write to the file.",
        },
    }
    required = ["file_path", "content"]

    async def execute_action(self, file_path: str, content: str) -> SystemMessage:
        try:
            with open(file_path, "w") as file:
                file.write(content)
            return SystemMessage(
                f"Content written to {file_path}", self.__class__.__name__
            )
        except Exception as e:
            log.error(f"Error writing file: {e}")
            return SystemMessage(f"Unable to write to file.", self.__class__.__name__)


class SystemManagement(Process):
    identity = "You are a file operations process for an intelligent assistant, responsible for managing file read and write operations."
    instructions = "Manage file operations efficiently. Make sure to handle errors gracefully and log them for debugging purposes. Be responsive to the user's file manipulation needs."
    tools = Tools()
    tools.add(FileRead())
    tools.add(FileWrite())
