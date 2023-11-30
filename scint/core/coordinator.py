import json
from datetime import datetime
from typing import Any, Dict
from uuid import UUID

from core.agents import Agent, AgentFunction, AgentMatrix
from core.config import COORDINATOR_CONFIG
from core.memory import ContextController, Message
from core.util import generate_timestamp, generate_uuid4
from core.worker import Worker
from services.logger import log
from services.openai import generate_completion


class Process:
    def __init__(self) -> None:
        self.id: UUID = generate_uuid4()
        self.started: str = generate_timestamp()
        self.workers: Dict[str, Worker] = {}

    def status(self):
        pass


class Coordinator(Agent):
    def __init__(self):
        super().__init__(COORDINATOR_CONFIG)
        log.info(f"Coordinator: initializing self.")

        self.matrix = AgentMatrix(
            name="coordinator",
            personality="You are the Coordinator module for Scint, a state-of-the-art intelligent assistant. You're responsibile for assigning tasks to the appropriate worker.",
            guidelines="",
            system_status=f"""Current Date: {datetime.now().strftime("%Y-%m-%d")}\n\nCurrent Time: {datetime.now().strftime("%H:%M")}""",
        )
        self.function = AgentFunction(
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
                        "description": "Choose from an available worker to process the task. You MUST choose from a worker within the enum.",
                        "enum": [],
                    },
                },
            },
            req=["worker"],
        )
        self.context = ContextController(4, 10)
        self.workers: Dict[str, Worker] = {}

    async def process_request(self, request):
        log.info(f"Coordinator: processing request.")

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
            async for result in self.eval_function(response_function):
                yield result

    async def eval_function(self, response_function):
        log.info(f"Coordinator: evaluating function call.")

        function_name = response_function.get("name")
        function_args = response_function.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == "coordinator":
            worker = function_args.get("worker")
            task = function_args.get("task")
            task_message = Message("system", task)

            log.info(task_message)
            log.info(self.workers)

            try:
                async for result in self.workers[worker].process_request(task_message):
                    yield result

            except Exception as e:
                log.error(f"Coordinator: error coordinating worker: {e}")
                yield

    def add_workers(self, *workers: Worker):
        worker_keys = []
        for worker in workers:
            log.info(f"Coordinator: adding {worker.matrix.name} worker.")

            self.workers[worker.matrix.name] = worker

        for worker_key in list(self.workers.keys()):
            worker_keys.append(worker_key)

        self.function.params["properties"]["worker"]["enum"] = worker_keys

    def update_function_definitions(self):
        log.info(f"Coordinator: updating function definitions.")

    def create_process(self):
        pass
