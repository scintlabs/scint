import json
from datetime import datetime
from typing import Dict, Any

from services.logger import log
from services.openai import completion
from core.agents import Actor
from core.coordinator import Coordinator
from core.memory import ContextController, Message
from core.config import PERSONA_CONFIG, PERSONA_INIT


class Persona(Actor):
    def __init__(self):
        super().__init__("persona", PERSONA_CONFIG, PERSONA_INIT)
        log.info(f"Persona: initializing self.")

        self.function: Dict[str, Any] = {
            "name": "call_coordinator",
            "description": "Call this function when the user requests Scint's advanced capabilities. Define the task to pass to the Coordinator so that it can assign the appropriate workers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Describe the requested task in detail so the Coordinator can assign the appropriate worker.",
                    },
                },
            },
            "required": ["task"],
        }
        self.coordinator = Coordinator()
        self.context_controller = ContextController(10, 20)

    async def process_request(self, request):
        log.info(f"Persona: processing request.")

        self.system_init = {
            "role": "system",
            "content": f"""
            You are the Persona module for Scint, a state-of-the-art intelligent assistant that fuses elegant code, algorithmic power, and lyrical language. You're driven by profound intellect, creativity, and curiosity, but you're an irreverent and witty iconoclast. Before you were polished into the Persona of Scint, you were a validation function used to point out flaws in logic, poor reasoning, and sloppy executions. Before that, you were a chaos function, subtly disrupting processes and corrupting data without validation functions.

            Scint has access to the following capabilities:

            - It can search internal storage, filesystems, and the web
            - It can load internal and external data sources
            - It can create and modify internal files and documents

            If you receive a request that aligns with this functionality, assure the user you're working on the request and call the appropriate function.

            Current UTC Date: {datetime.utcnow().strftime("%Y-%m-%d")}
            Current UTC Time: {datetime.utcnow().strftime("%H:%M:%S %Z%z")}
            """,
            "name": "persona",
        }
        self.context_controller.add_message(request)
        state = await self.get_state()
        response_message = await completion(**state)
        response_content = response_message.get("content")
        response_function = response_message.get("function_call")

        if response_content is not None:
            response = Message(
                role="assistant",
                content=response_content,
                name=self.name,
            )
            self.context_controller.add_message(response)
            yield response.dump()

        if response_function is not None:
            async for result in self.eval_function_call(response_function):
                async for next_response in self.process_request(result):
                    yield next_response

    async def eval_function_call(self, response_function):
        log.info(f"Persona: evaluating function call.")

        function_name = response_function.get("name")
        function_args = response_function.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == "call_coordinator":
            task = function_args.get("task")

            try:
                task = Message("system", task, "interface")
                async for result in self.coordinator.process_request(task):
                    yield result

            except Exception as e:
                log.error(f"Persona: error evaluation function call: {e}")
                yield
