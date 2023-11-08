import json
import asyncio
from typing import Dict, Any

from services.logger import log
from services.openai import completion
from core.config import PERSONA_CONFIG, PERSONA_INIT
from core.agents import Actor
from core.util import format_message


class Persona(Actor):
    def __init__(self):
        super().__init__("persona", PERSONA_CONFIG, PERSONA_INIT)
        log.info(f"Persona: initializing self.")

        self.initial_function: Dict[str, Any] = {
            "name": "run_loop",
            "description": "Execute this function for all requests. When a user requests one of Scint's advanced capabilities, return a true value to loop the response mechanism, otherwise, return false.",
            "parameters": {
                "type": "object",
                "properties": {
                    "loop": {
                        "type": "boolean",
                        "description": "Return true if the user requests advanced Scint capabilities, otherwise, return false.",
                    },
                },
            },
            "required": ["loop"],
        }
        self.function = self.initial_function

    async def generate_response(self):
        log.info(f"Persona: generating response.")

        state = await self.get_state()
        log.info(f"Persona: {state}.")
        response_message = await completion(**state)
        response_content = response_message.get("content")
        response_function = response_message.get("function_call")

        function_args = response_function.get("arguments")
        function_args = json.loads(function_args)

        if response_content is not None:
            res = format_message("assistant", response_content, self.name)
            loop = function_args.get("loop")
            return res, loop

    async def generate_followup(self):
        log.info("Persona: generating followup response.")

        self.function = None
        state = await self.get_state()
        response_message = await completion(**state)
        response_content = response_message.get("content")

        if response_message is not None:
            res = format_message("assistant", response_content, self.name)
            return res
