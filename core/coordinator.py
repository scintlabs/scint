import json
import random
from typing import List, Dict, Any

from services.logger import log
from services.openai import completion
from core.config import WORKER_PROCESSING_MESSAGES, COORDINATOR_INIT, COORDINATOR_CONFIG
from core.worker import Worker
from core.agents import Actor
from core.operator import Operator
from core.util import format_message


async def execute_control_flow(context, *workers):
    for worker in workers:
        context = await worker.process_request(context)
    return context


class Coordinator(Actor):
    def __init__(self):
        super().__init__("coordinator", COORDINATOR_CONFIG, COORDINATOR_INIT)
        log.info(f"Coordinator: initializing self.")

        self.function: Dict[str, Any] = {
            "name": "coordinator",
            "description": "Define and classify the user's request and assign it to the appropriate worker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Based on the request, define a task for the worker. Avoid ambiguity and be specific.",
                    },
                    "classification": {
                        "type": "string",
                        "description": "Classify the type of request being made.",
                        "enum": [
                            "general_discussion",
                            "information_request",
                            "control_flow_operation",
                        ],
                    },
                    "worker": {
                        "type": "string",
                        "description": "Select the appropriate worker based on the task and request. For general discussion or tasks that don't require a worker, return 'operator' for the worker.",
                        "enum": [],
                    },
                },
            },
            "required": ["task", "classification"],
        }
        self.workers: Dict[str, Worker] = {}
        self.control_flows: Dict[str, List[Worker]] = {}
        self.current_flow: Dict[str, int] = {}
        self.operator = Operator()

    def add_workers(self, *workers: Worker):
        for worker in workers:
            log.info(f"Coordinator: adding {worker.name} worker.")
            self.workers[worker.name] = worker

        self.update_function_definitions()

    def update_function_definitions(self):
        log.info(f"Coordinator: updating function definitions.")
        self.function["parameters"]["properties"]["worker"]["enum"] = list(
            self.workers.keys()
        )

    def add_control_flows(self, control_flows: Dict[str, List[Worker]]):
        for process_name, flow in control_flows.items():
            log.info(f"Coordinator: Adding {process_name} control flow process.")
            self.control_flows[process_name] = flow

        self.update_function_definitions()

    def update_flow_state(self, flow_name: str):
        log.info(f"Coordinator: updating flow state for {flow_name}.")

        if flow_name in self.current_flow:
            self.current_flow[flow_name] += 1
            if self.current_flow[flow_name] >= len(self.control_flows[flow_name]):
                del self.current_flow[flow_name]

    def get_next_worker_in_flow(self, flow_name: str) -> Worker:
        log.info(f"Coordinator: getting next worker for {flow_name}.")

        if flow_name not in self.current_flow:
            self.current_flow[flow_name] = 0

        step_index = self.current_flow[flow_name]
        return self.control_flows[flow_name][step_index]

    async def generate_response(self, request):
        log.info(f"Coordinator: processing request: {request}")

        await self.context_controller.add_message(request)
        state = await self.get_state()
        response = await completion(**state)
        function_call = response.get("function_call")

        if function_call is not None:
            async for chunk in self.call_function(response, request):
                yield chunk

        else:
            yield response

    async def call_function(self, res_message, original_request):
        log.info(f"Coordinator: evaluating function call.")

        function_call = res_message.get("function_call")

        if not function_call:
            yield {"error": "Coordinator: No function call"}

        function_name = function_call.get("name")
        function_args = function_call.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == self.name:
            task = function_args.get("task")
            classification = function_args.get("classification")
            worker = function_args.get("worker")

            try:
                if worker.strip() == "operator":
                    res = await self.operator.generate_response()
                    yield res

                else:
                    processing_message = random.choice(list(WORKER_PROCESSING_MESSAGES))
                    formatted_message = format_message(
                        "system", processing_message, self.name
                    )
                    yield formatted_message

                    worker_name = worker.strip()
                    task = format_message("system", task, self.name)
                    task_result = await self.workers[worker_name].generate_response(
                        task
                    )
                    context = [original_request]
                    context.append(task_result)
                    final_res = await self.operator.generate_response(context)

                    yield final_res

            except Exception as e:
                log.error(f"Error coordinating worker: {e}")
                yield {"error": f"Error coordinating worker: {e}"}
        else:
            log.error("Function name is not 'coordinator'.")
            yield {"error": "Function name is not 'coordinator'."}
