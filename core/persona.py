from services.logger import log
from services.openai import completion
from core.config import PERSONA_CONFIG, PERSONA_INIT
from core.agents import Actor
from core.util import format_message


class Persona(Actor):
    def __init__(self):
        super().__init__("persona", PERSONA_CONFIG, PERSONA_INIT)
        log.info(f"Persona: initializing self.")

        self.function = None

    async def generate_response(self):
        log.info(f"Persona: processing request.")

        state = await self.get_state()
        response_message = await completion(**state)
        response_content = response_message.get("content")

        if response_content is not None:
            res = format_message("assistant", response_content, self.name)
            return res
