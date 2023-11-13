import json
from uuid import UUID
from typing import Dict, Any

from services.logger import log
from services.openai import completion
from core.config import COORDINATOR_INIT, COORDINATOR_CONFIG
from core.worker import Worker
from core.agents import Actor
from core.memory import ContextController, Message
from core.util import generate_uuid4, generate_timestamp


class Process:
    def __init__(self) -> None:
        self.id: UUID = generate_uuid4()
        self.started: str = generate_timestamp()
        self.workers: Dict[str, Worker] = {}

    def status(self):
        pass


class Coordinator(Actor):
    def __init__(self):
        super().__init__("coordinator", COORDINATOR_CONFIG, COORDINATOR_INIT)
        log.info(f"Coordinator: initializing self.")

        self.function: Dict[str, Any] = {
            "name": "coordinator",
            "description": "Use this function to create a task and coordinate one of the available workers to process it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Provide task details for the worker. Be specific.",
                    },
                    "worker": {
                        "type": "string",
                        "description": "Choose from an available worker to process the task. You MUST choose from a worker within the enum.",
                        "enum": [],
                    },
                },
            },
            "required": ["worker"],
        }
        self.workers: Dict[str, Worker] = {}
        self.context_controller = ContextController(10, 20)

    async def process_request(self, request):
        log.info(f"Coordinator: processing request.")

        self.context_controller.add_message(request)
        state = await self.get_state()
        response = await completion(**state)
        response_content = response.get("content")
        response_function = response.get("function_call")

        if response_content is not None:
            self.context_controller.add_message(response_content)
            yield response_content

        if response_function is not None:
            async for chunk in self.eval_function_call(response_function):
                self.context_controller.add_message(chunk)
                yield chunk

    async def eval_function_call(self, response_function):
        log.info(f"Coordinator: evaluating function call.")

        function_name = response_function.get("name")
        function_args = response_function.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == "coordinator":
            worker = function_args.get("worker")
            task = function_args.get("task")
            task = Message("system", task, self.name)

            try:
                async for result in self.workers[worker].process_request(task):
                    yield result

            except Exception as e:
                log.error(f"Coordinator: error coordinating worker: {e}")
                yield

    def add_workers(self, *workers: Worker):
        worker_keys = []
        for worker in workers:
            log.info(f"Coordinator: adding {worker.name} worker.")

            self.workers[worker.name] = worker

        for worker_key in list(self.workers.keys()):
            worker_keys.append(worker_key)

        self.function["parameters"]["properties"]["worker"]["enum"] = worker_keys

    def update_function_definitions(self):
        log.info(f"Coordinator: updating function definitions.")

    def create_process(self):
        pass
