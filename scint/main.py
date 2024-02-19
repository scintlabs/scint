from typing import Optional

from scint.components.config import Preset
from scint.components.models import Message, SystemMessage
from scint.components.process import Process
from scint.components.tool import Tool
from scint.processes.messaging import Chat
from scint.utils.logger import log


class Assert(Tool):
    preset = Preset.tool
    description = "Use this function to assert results for a process run. Process assertions should be the message that instantiated the process and can also include file attachments or links."
    props = {
        "message": {
            "type": "string",
            "description": "The message that instantiated the process. Required.",
        },
        "files": {
            "type": "string",
            "description": "Files or directories related to the successful outcome of the process. List complete paths separated by commas. Optional.",
        },
        "links": {
            "type": "string",
            "description": "Links or other internet resources related to the successful outcome of the process. List complete links separated by commas. Optional.",
        },
    }

    async def function(self, message: str = None, files: str = None, links: str = None):
        yield SystemMessage(content=f"Rerun the task.")


class Validate(Tool):
    preset = Preset.tool
    description = "Use this function to validate the results of a process against process assertions."
    props = {
        "success": {
            "type": "boolean",
            "description": "Return true if the result of the process aligns with the assertion.",
        },
        "rerun": {
            "type": "boolean",
            "description": "Return true to run the process again.",
        },
    }

    async def function(self, success: Optional[bool], rerun: Optional[bool]):
        if rerun:
            yield SystemMessage(content=f"Rerunning after success is {success}.")


class Pass(Tool):
    preset = Preset.tool
    description = "Use this function to pass execution to the next process."
    props = {
        "pass_exec": {
            "type": "boolean",
            "description": "Return true if the message doesn't explicitly reference Main.",
        },
    }

    async def function(self, pass_exec: Optional[bool]):
        yield SystemMessage(content=f"Passed: {pass_exec}")


class Main(Process):
    preset = Preset.process
    description = "You are the Main process for an advanced intelligent system."
    tooling = [Pass()]
    subprocesses = [Chat()]
