import json
import importlib
from typing import Dict, List, Any

from services.logger import log
from services.openai import completion
from core.config import PERSONA_INIT, PERSONA_CONFIG
from core.agent import Agent


class Persona(Agent):
    def __init__(self):
        log.info(f"Persona: initializing self.")

        self.name = "persona"
        self.system_init: Dict[str, str] = PERSONA_INIT
        self.config: Dict[str, Any] = PERSONA_CONFIG
        self.context: List[Dict[str, str]] = [self.system_init]
        self.function = None

    async def process_request(self, context: List[dict[str, str]]):
        log.info(f"Persona: processing request.")

        for item in context:
            self.context.append(item)

        state = await self.get_state()
        res = await completion(**state)

        if not isinstance(res, dict):
            log.error("res_message is not a dictionary.")
            return

        content = res.get("content")

        if content is not None:
            reply = await self.format_message("assistant", content, self.name)
            return reply
