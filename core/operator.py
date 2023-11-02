from typing import Dict, List

from services.logger import log
from services.openai import completion
from core.config import OPERATOR_INIT, OPERATOR_CONFIG
from core.agents import Actor
from core.util import format_message


class Operator(Actor):
    def __init__(self):
        super().__init__("operator", OPERATOR_CONFIG, OPERATOR_INIT)
        log.info(f"Operator: initializing self.")

        self.function = None

    async def generate_response(self):
        log.info(f"Operator: processing request.")

        state = await self.get_state()
        log.info(f"{self.state}")
        res = await completion(**state)
        content = res.get("content")

        if content is not None:
            reply = format_message("assistant", content, self.name)
            await self.context_controller.add_message(reply)
            return reply
