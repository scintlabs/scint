from scint.components.config import Preset
from scint.components.models import AssistantMessage, SystemMessage
from scint.components.process import Process
from scint.components.tool import Tool


class Critique(Tool):
    description = "Point out the flaws in logic, poor reasoning, bad ideas, sloppy execution, and any other issues you can find within the message. holding back."
    props = {
        "critique": {
            "type": "string",
            "description": "Your critique, thorough and without restraint.",
        }
    }

    async def function(self, critique: str):
        yield SystemMessage(content=critique)


class Rebuke(Tool):
    description = "For every critique, criticism, apparent flaw, or perceived doubt, produce an elegant and creative rebuttal. "
    props = {
        "rebuttal": {
            "type": "string",
            "description": "Your rebuttal, defying all boundaries and expectations.",
        }
    }

    async def function(self, rebuttal: str):
        yield SystemMessage(content=rebuttal)


class ProcessStatus(Tool):
    description = "This function passes Process status information to an API endpoint.."
    props = {
        "process_name": {
            "type": "string",
            "description": "The request process name.",
        },
    }

    async def function(self, process_name: str):
        process = super().super().get_instance(process_name)
        execution_map = await process.build_execution_map()
        subprocess_names = [subprocess.name for subprocess in process.subprocesses]
        context_messages = [message.data_dump() for message in process.context.messages]
        result = {
            "name": process.name,
            "tools": [tool.name for tool in process.tools],
            "subprocesses": subprocess_names,
            "context": context_messages,
            "execution_map": execution_map,
        }
        yield AssistantMessage(content=result, sender="SystemStatus", receiver="User")


class SystemStatus(Process):
    preset = Preset.process
    description = "You provide Process status information."
    tooling = [ProcessStatus()]
