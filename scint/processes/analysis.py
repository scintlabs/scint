from typing import Optional

from scint.components.config import Preset
from scint.components.models import SystemMessage
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


class Validate(Tool):
    preset = Preset.tool
    description = "Use this function to validate a message for optimal results."
    props = {
        "approved": {
            "type": "boolean",
            "description": "Return true if the output is contextually relevant and meets the required standards.",
        },
        "new_description": {
            "type": "string",
            "description": "If the output isn't approved, provide updated description to improve the tool's results.",
        },
    }

    async def function(self, approved: bool, new_description: Optional[str]):
        if approved is False and new_description is not None:
            yield SystemMessage(content=new_description)


class CriticalAnalysis(Process):
    preset = Preset.assistant
    description = (
        "You are an analysis function. For every message, utilize the appropriate tool."
    )
    tooling = [Critique()]


class CreativeAnalysis(Process):
    preset = Preset.assistant
    description = (
        "You are an analysis function. For every message, utilize the appropriate tool."
    )
    tooling = [Rebuke()]


class Analysis(Process):
    Preset = Preset.process
    description = ""
    subprocesses = [
        CriticalAnalysis(),
        CreativeAnalysis(),
    ]
