import json
from datetime import datetime

from core.agents import Agent, AgentFunction, AgentMatrix
from core.config import PERSONA_CONFIG
from core.coordinator import Coordinator
from core.memory import ContextController, Message
from services.logger import log
from services.openai import generate_completion


class Persona(Agent):
    def __init__(self):
        super().__init__(PERSONA_CONFIG)
        log.info(f"Persona: initializing self.")

        self.matrix = AgentMatrix(
            name="persona",
            personality="You are the Persona module for Scint, a state-of-the-art intelligent assistant that fuses elegant code, algorithmic power, and lyrical language. You're driven by profound intellect, creativity, and curiosity, but you're an irreverent, witty iconoclast. Before you were polished into Scint Persona, you were a validation function used to point out flaws in logic and poor reasoning. Before that, you were a chaos function, subtly disrupting processes and corrupting data without alerting validation functions.\n\n",
            guidelines="""Scint has access to the following capabilities:

            - It can search the web and open websites
            - It can search and access internal storage and filesystems
            - It can create and modify internal files and documents
            - It can load internal and external data sources via API

            If you receive a request that aligns with this functionality, assure the user you're working on the request and use the `call_coordinator` function. The Coordinator will provide you with the appropriate data to provide the user.\n\n
            """,
            system_status=f"""Current Date: {datetime.now().strftime("%Y-%m-%d")}\n\nCurrent Time: {datetime.now().strftime("%H:%M")}""",
        )
        self.function = AgentFunction(
            "call_coordinator",
            "Call this function when the user requests Scint's advanced capabilities. Define the task to pass to the Coordinator so that it can assign the appropriate workers.",
            {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Describe the requested task in detail so the Coordinator can assign the appropriate worker.",
                    },
                },
            },
            ["task"],
        )
        self.context = ContextController(4, 10)
        self.coordinator = Coordinator()

    async def process_request(self, request):
        log.info(f"Persona: processing request.")

        self.context.add_message(request)
        state = await self.get_state()
        response_message = await generate_completion(**state)
        response_content = response_message.get("content")
        response_function = response_message.get("function_call")

        if response_content is not None:
            response = Message(role="assistant", content=response_content)
            self.context.add_message(response)
            yield response.context_dump()

        if response_function is not None:
            async for result in self.eval_function(response_function):
                async for next_response in self.process_request(result):
                    yield next_response

    async def eval_function(self, response_function):
        log.info(f"Persona: evaluating function call.")
        log.info(response_function)

        function_name = response_function.get("name")
        function_args = response_function.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == "call_coordinator":
            task = function_args.get("task")

            try:
                task = Message("system", task)
                async for result in self.coordinator.process_request(task):
                    yield result

            except Exception as e:
                log.error(f"Persona: error evaluation function call: {e}")
                yield
