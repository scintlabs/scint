import importlib
import json
from datetime import datetime

from scint.core.agents import Agent, AgentTool, AgentMatrix
from scint.core.config import DEFAULT_CONFIG
from scint.core.memory import ContextController, Message
from scint.services.logger import log
from scint.services.openai import generate_completion


class WorkerTool(AgentTool):
    def __init__(self):
        super().__init__(
            name="coordinator",
            desc="Use this function to create a task and coordinate one of the available workers to process it.",
            params={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Provide task details for the worker. Be specific.",
                    },
                    "worker": {
                        "type": "string",
                        "description": "Choose from the available workers to process the task.",
                        "enum": [],
                    },
                },
            },
            req=["worker"],
        )

    async def function(self, **kwargs):
        log.info(f"Coordinator: evaluating function call.")
        pass


class WorkerMatrix(AgentMatrix):
    def __init__(self):
        super().__init__(
            name="coordinator",
            personality="You are the Coordinator module for Scint, a state-of-the-art intelligent assistant. You're responsibile for assigning tasks to the appropriate worker.",
            guidelines="",
            system_status=f"""Current Date: {datetime.now().strftime("%Y-%m-%d")}\n\nCurrent Time: {datetime.now().strftime("%H:%M")}""",
        )


class Worker(Agent):
    def __init__(self, name, purpose, description, params, req):
        super().__init__(DEFAULT_CONFIG)

        log.info(f"Worker: initializing {name}.")

        self.matrix = WorkerMatrix(name=name, personality=purpose)
        self.tool = WorkerTool(name=name, desc=description, params=params, req=req)
        self.context = ContextController(2, 4)

    async def process_request(self, request: Message) -> Message:
        log.info(f"Worker: processing request.")

        self.context.add_message(request)
        state = await self.get_state()
        response_message = await generate_completion(**state)
        response_content = response_message.get("content")
        response_function = response_message.get("function_call")

        if response_content is not None:
            response = Message(role="system", content=response_content)
            self.context.add_message(response)
            yield response

        if response_function is not None:
            async for chunk in self.eval_tool_call(response_function):
                self.context.add_message(chunk)
                yield chunk
