import json
import asyncio
from typing import Dict, Any

from services.logger import log
from services.openai import completion
from core.config import COORDINATOR_INIT, COORDINATOR_CONFIG
from core.worker import Worker
from core.agents import Actor
from core.persona import Persona
from core.util import format_message


class Coordinator(Actor):
    def __init__(self):
        super().__init__("coordinator", COORDINATOR_CONFIG, COORDINATOR_INIT)
        log.info(f"Coordinator: initializing self.")

        self.function: Dict[str, Any] = {
            "name": "coordinator",
            "description": "Summarize and classify the user request and define a task for responding to it. If the user requests a task that corresponds with an available worker, assign the task to that worker. Otherwise, do not assign a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Define a task for the worker. Avoid ambiguity and be specific.",
                    },
                    "classification": {
                        "type": "string",
                        "description": "Classify the type of request being made.",
                        "enum": [
                            "information_request",
                            "task_completion",
                            "miscellaneous",
                        ],
                    },
                    "worker": {
                        "type": "string",
                        "description": "Select the appropriate worker based on the task and request.",
                        "enum": [],
                    },
                },
            },
            "required": ["task", "classification"],
        }
        self.workers: Dict[str, Worker] = {}
        self.persona = Persona()

    async def process_request(self, request):
        log.info(f"Coordinator: processing request.")

        self.context_controller.add_message(request)
        state = await self.get_state()
        response_function, response_message = await asyncio.gather(
            completion(**state),
            self.persona.generate_response(),
        )

        if response_message is not None:
            self.context_controller.add_message(response_message)
            yield response_message

        if response_function.get("function_call") is not None:
            async for chunk in self.call_function(response_function):
                self.context_controller.add_message(chunk)
                func_assistant_message = await self.persona.generate_response()
                yield func_assistant_message

    async def call_function(self, response):
        log.info(f"Coordinator: evaluating function call.")

        function_call = response.get("function_call")
        function_name = function_call.get("name")
        function_args = function_call.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == self.name:
            task = function_args.get("task")
            worker = function_args.get("worker").strip()

            try:
                task = format_message("system", task, self.name)

                async for chunk in self.workers[worker].process_request(task):
                    yield chunk

            except Exception as e:
                log.error(f"Coordinator: error coordinating worker: {e}")
                yield format_message(
                    "system", f"Error coordinating worker: {e}", self.name
                )

        else:
            log.error("Coordinator: function name is not 'coordinator'.")
            yield format_message("system", "No function initialized.", self.name)

    def add_workers(self, *workers: Worker):
        for worker in workers:
            log.info(f"Coordinator: adding {worker.name} worker.")
            self.workers[worker.name] = worker

        self.update_function_definitions()

    def update_function_definitions(self):
        log.info(f"Coordinator: updating function definitions.")

        workers = []

        for worker in list(self.workers.keys()):
            workers.append(worker)

        self.function["parameters"]["properties"]["worker"]["enum"] = workers
