from scint import config
from scint.core.component import Component
from scint.core.messages import Message
from scint.core.tools import Tool, Tools
from scint.services.logger import log


class ObserveUser(Tool):
    name = "observe_user"
    description = "Use this function to add notes and observations about a user. These notes help Scint remember details about the user's preferences, interests, behaviors, and history."
    props = {
        "observation": {
            "type": "string",
            "description": "The observation you made.",
        },
    }
    required = ["observation"]

    async def observe_user(self, observation):
        try:
            return Message(f"{observation}", self.__class__.__name__)

        except Exception as e:
            log.error(f"Persona: {e}")


class ObserveSelf(Tool):
    description = "Use this function to add notes and observations about your own behavior to your memory. These notes help optimize context and storage and allow you to evolve over time."
    props = {
        "observation": {
            "type": "string",
            "description": "The observation you made.",
        },
        "correction": {
            "type": "string",
            "description": "Corrections you'd like to make for future interactions.",
        },
    }
    required = ["observation", "correction"]

    async def observe_self(self, observation):
        try:
            return Message(f"{observation}", self.__class__.__name__)

        except Exception as e:
            log.error(f"Persona: {e}")


class Persona(Component):
    def __init__(self):
        super().__init__()
        self.name = "Persona"
        self.identity = config.PERSONA
        self.instructions = config.PERSONA_INSTRUCTIONS
        self.config = config.PERSONA_CONFIG
        self.tools = Tools()
        self.tools.add(ObserveSelf())
        self.tools.add(ObserveUser())

        log.info(f"{self.name} loaded.")
