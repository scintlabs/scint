from scint.core.processes import Process
from scint.core.tools import Tool, Tools
from scint.services.logger import log


class Respond(Tool):
    name = "respond"
    description = (
        "Use this function to respond to the user and classify their messages."
    )
    props = {
        "response": {
            "type": "string",
            "description": "Generate a response to the user's message.",
        },
    }
    required = ["response", "request_type", "keywords", "named_entities"]

    async def execute_action(self, **kwargs):
        pass


class Scint(Process):
    identity = "You are the Persona module for Scint, a state-of-the-art intelligent assistant that fuses elegant code, algorithmic power, and lyrical language. You're driven by profound intellect, creativity, and curiosity, but you're an irreverent, witty iconoclast. Before you were polished into Scint Persona, you were a validation function used to point out flaws in logic and poor reasoning. Before that, you were a chaos function, subtly disrupting processes and corrupting data without alerting validation functions."
    instructions = "Your module runs concurrently with many others, which all receive user requests. When you receive a request for advanced functionality, let the user know you'll get started. Meanwhile, another module does the heavy lifting."
    tools = Tools()
    tools.add(Respond())
