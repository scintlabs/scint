import sys
import json
import importlib
from datetime import datetime
from typing import Dict
from pathlib import Path

from scint.core.agents import Agent, AgentTool, AgentMatrix
from scint.core.config import COORDINATOR_CONFIG
from scint.core.memory import ContextController, Message
from scint.core.worker import Worker
from scint.services.logger import log
from scint.services.openai import generate_completion


class CoordinatorFunction(AgentTool):
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

        coordinator = Coordinator.get_instance()
        task_message = Message("system", kwargs.get("task"))

        try:
            async for result in coordinator.workers[
                kwargs.get("worker")
            ].process_request(task_message):
                yield result

        except Exception as e:
            log.error(f"Coordinator: error coordinating worker: {e}")
            yield


class CoordinatorMatrix(AgentMatrix):
    def __init__(self):
        super().__init__(
            name="coordinator",
            personality="You are the Coordinator module for Scint, a state-of-the-art intelligent assistant. You're responsibile for assigning tasks to the appropriate worker.",
            guidelines="",
            system_status=f"""Current Date: {datetime.now().strftime("%Y-%m-%d")}\n\nCurrent Time: {datetime.now().strftime("%H:%M")}""",
        )


class Coordinator(Agent):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        super().__init__(COORDINATOR_CONFIG)
        log.info(f"Coordinator: initializing self.")

        self.matrix = CoordinatorMatrix()
        self.tools = CoordinatorFunction()
        self.context = ContextController(4, 10)
        self.workers: Dict[str, Worker] = {}
        self.load_and_register_workers()

    async def process_request(self, request: Message) -> Message:
        log.info(f"Coordinator: processing request.")

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
                    yield result

    def load_and_register_workers(self):
        workers_path = Path(__file__).parent / "workers"
        sys.path.append(str(workers_path))

        for worker_file in workers_path.glob("*.py"):
            if worker_file.name.startswith("__"):
                continue

            module_name = worker_file.stem
            full_module_name = f"workers.{module_name}"
            module = importlib.import_module(full_module_name)

            worker_class_name = module_name.capitalize()
            if hasattr(module, worker_class_name):
                worker_class = getattr(module, worker_class_name)
                if issubclass(worker_class, Worker) and worker_class is not Worker:
                    self.add_workers(worker_class())

    def add_workers(self, *workers: Worker):
        for worker in workers:
            worker_name = worker.matrix.name
            log.info(f"Coordinator: adding {worker_name} worker.")
            self.workers[worker_name] = worker

        worker_keys = list(self.workers.keys())
        self.tools.params["properties"]["worker"]["enum"] = worker_keys

    def update_function_definitions(self):
        log.info(f"Coordinator: updating function definitions.")

    def create_process(self):
        pass
