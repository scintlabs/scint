import json
from datetime import datetime

from scint.core.agents import Agent, AgentMatrix, AgentTool
from scint.core.config import PERSONA_CONFIG
from scint.core.coordinator import Coordinator
from scint.core.memory import ContextController, Message
from scint.services.logger import log
from scint.services.openai import generate_completion


class PersonaFunction(AgentTool):
    def __init__(self):
        super().__init__(
            name="subroutine",
            desc="Call this function to activate the necessary subroutines when a user requests Scint's advanced capabilities.",
            params={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Describe the requested task in detail so the Coordinator can assign the appropriate worker.",
                    },
                },
            },
            req=["task"],
        )
        self.coordinator = Coordinator.get_instance()

    async def function(self, **kwargs):
        log.info(f"Persona: calling function.")

        try:
            task = Message("system", kwargs.get("task"))
            async for result in self.coordinator.process_request(task):
                yield result

        except Exception as e:
            log.error(f"Persona: error calling function: {e}")
            yield


class PersonaMatrix(AgentMatrix):
    def __init__(self):
        super().__init__(
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


class Persona(Agent):
    def __init__(self):
        super().__init__(PERSONA_CONFIG)
        log.info(f"Persona: initializing self.")

        self.matrix = PersonaMatrix()
        self.tools = PersonaFunction()
        self.context = ContextController(4, 10)

    async def process_request(self, request: Message) -> Message:
        log.info(f"Persona: processing request.")

        self.context.add_message(request)
        state = await self.get_state()
        response_message = await generate_completion(**state)
        response_message_content = response_message.get("content")
        tool_calls = response_message.get("tool_calls")

        if response_message_content is not None:
            response = Message(role="assistant", content=response_message_content)
            self.context.add_message(response)
            yield response

        if tool_calls is not None:
            for tool_call in tool_calls:
                function = tool_call.get("function")
                function_name = function.get("name")
                function_args = json.loads(function.get("arguments"))

                async for result in self.tools.evaluate(function_name, **function_args):
                    async for next_response in self.process_request(result):
                        yield next_response
