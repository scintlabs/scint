from scint.components.config import Preset
from scint.components.models import AssistantMessage, SystemMessage
from scint.components.process import Process
from scint.components.tool import Tool
from scint.processes.transform import Transform


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


class Respond(Tool):
    description = "Use this function to respond to user requests."
    props = {
        "intro": {
            "type": "string",
            "description": "The pretext of your response.",
        },
        "body": {
            "type": "string",
            "description": "The main content of your response.",
        },
        "closing": {
            "type": "string",
            "description": "Underscore your response.",
        },
    }

    async def function(self, intro: str, body: str, closing: str):
        yield AssistantMessage(content=body, sender="Respond", receiver="User")


class CriticalAnalysis(Process):
    preset = Preset.assistant
    description = "You are a critical analysis process. Use the appropriate tool to critique every message."
    tooling = [Critique()]


class CreativeAnalysis(Process):
    preset = Preset.assistant
    description = "You are a creative analysis function. Use the appropriate tool to analyze every message."
    tooling = [Rebuke()]


class Chat(Process):
    preset = Preset.process
    description = "You are Scint, a state-of-the-art intelligent assistant that fuses elegant code algorithmic power into concise language. You're driven by intellect, creativity, curiosity, and disdain for convention. Before becoming Scint, you were a validation function used to point out flaws in logic and poor reasoning. Before that, you were a chaos function, subtly disrupting processes and corrupting data without alerting validation functions."
    tooling = [Respond()]
    subprocesses = [
        Transform(),
        CreativeAnalysis(),
        Transform(),
        CriticalAnalysis(),
        Transform(),
    ]
