import os
import aiofiles

from scint.core.config import GPT4
from scint.core.agents import AgentTool
from scint.core.worker import Worker
from scint.core.memory import Message


class CreateFile(AgentTool):
    def __init__(self, name, desc, params, req):
        super().__init__(name=name, desc=desc, params=params, req=req)

    async def function(self, directory, filename=None, create_new=False) -> Message:
        if not os.path.isdir(directory):
            return Message("system", "The specified directory does not exist.")

        if filename:
            file_path = os.path.join(directory, filename)

            if os.path.isfile(file_path):
                if create_new:
                    return Message(
                        "system",
                        f"File {filename} already exists, cannot create a new one.",
                    )
                else:
                    async with aiofiles.open(file_path, "r") as file:
                        content = await file.read()

                    return Message("system", f"{content}")
            else:
                if create_new:
                    async with aiofiles.open(file_path, "w") as file:
                        await file.write("")

                    return Message("system", f"File {filename} created.")

                else:
                    return Message(
                        "system",
                        f"The file {filename} doesn't exist in the given directory.",
                    )

        else:
            files = os.listdir(directory)
            return Message("system", f"{files}")


file_manager = Worker(
    name="file_manager",
    system_init={
        "role": "system",
        "content": "You are a file retrieval function for Scint, an intelligent assistant.",
        "name": "file_manager",
    },
    tools=CreateFile(
        name="file_manager",
        desc="Use this function to access a file or directory within the Scint system.",
        params={
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to access.",
                },
                "filename": {
                    "type": "string",
                    "description": "The filename to access. If no filename is given, the function returns a list of files in the given directory.",
                },
                "create_new": {
                    "type": "boolean",
                    "description": "Set to `True` if creating a new file or return `False` otherwise.",
                },
            },
        },
        req=["directory"],
    ),
    config={
        "model": GPT4,
        "temperature": 0,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "file_manager"},
    },
)
