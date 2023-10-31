import json
import random
from typing import List, Dict, Any

from services.logger import log
from services.openai import completion
from core.config import GPT4, WORKER_PROCESSING_MESSAGES
from core.persona import Persona
from core.worker import Worker
from core.agent import Agent


async def execute_control_flow(context, *workers):
    for worker in workers:
        context = await worker.process_request(context)
    return context


class Coordinator(Agent):
    def __init__(self):
        log.info(f"Coordinator: initializing self.")

        self.name = "coordinator"
        self.system_init: Dict[str, str] = {
            "role": "system",
            "content": "You are the Coordinator module for Scint, an intelligent assistant. You're responsibile for classifying all incoming requests and assigning them to the appropriate worker OR control flow process.",
            "name": "coordinator",
        }
        self.function: Dict[str, Any] = {
            "name": "coordinator",
            "description": "Define and classify the user's request and assign it to the appropriate worker OR control flow process. For control flow operations, choose a control flow process, otherwise choose a worker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Based on the request, define a task for the worker OR the control flow process. Avoid ambiguity and be specific.",
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
                    "control_flow_process": {
                        "type": "string",
                        "description": "Select the appropriate control flow process based on the task and request.",
                        "enum": [],
                    },
                    "worker": {
                        "type": "string",
                        "description": "Select the appropriate worker based on the task and request. For general discussion or tasks that don't require a worker, return 'persona' for the worker.",
                        "enum": [],
                    },
                },
            },
            "required": ["task", "classification"],
        }
        self.config: Dict[str, Any] = {
            "model": GPT4,
            "temperature": 0,
            "top_p": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "function_call": {"name": "coordinator"},
        }
        self.workers: Dict[str, Worker] = {}
        self.control_flows: Dict[str, List[Worker]] = {}
        self.current_flow: Dict[str, int] = {}
        self.persona = Persona()

    async def process_request(self, request):
        log.info(f"Coordinator: processing request: {request}")

        self.context = [self.system_init]
        self.context.append(request)
        state = await self.get_state()
        response = await completion(**state)
        function_call = response.get("function_call")

        if function_call is not None:
            async for chunk in self.eval_function_call(response, request):
                yield chunk

        else:
            yield response

    async def eval_function_call(self, res_message, original_request):
        log.info("Coordinator: evaluating function call.")

        function_call = res_message.get("function_call")

        if not function_call:
            yield {"error": "No function call"}

        function_name = function_call.get("name")
        function_args = function_call.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == self.name:
            task = function_args.get("task")
            classification = function_args.get("classification")
            control_flow_process = function_args.get("control_flow_process")
            worker = function_args.get("worker")

            try:
                if worker.strip() == "persona":
                    context = [original_request]
                    context.append(res_message)
                    res = await self.persona.process_request(context)
                    yield res

                else:
                    processing_message = random.choice(list(WORKER_PROCESSING_MESSAGES))
                    formatted_message = await self.format_message(
                        "system", processing_message, self.name
                    )
                    yield formatted_message

                    worker_name = worker.strip()
                    task = await self.format_message("system", task, self.name)
                    task_result = await self.workers[worker_name].process_request(task)
                    context = [original_request]
                    context.append(task_result)
                    final_res = await self.persona.process_request(context)

                    if control_flow_process:
                        self.update_flow_state(control_flow_process)

                    yield final_res

            except Exception as e:
                log.error(f"Error coordinating worker: {e}")
                yield {"error": f"Error coordinating worker: {e}"}
        else:
            log.error("Function name is not 'coordinator'.")
            yield {"error": "Function name is not 'coordinator'."}

    def add_workers(self, *workers: Worker):
        for worker in workers:
            log.info(f"Coordinator: adding {worker.name} worker.")
            self.workers[worker.name] = worker

        self.update_function_definitions()

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

    def update_function_definitions(self):
        log.info(f"Coordinator: updating function definitions.")
        self.function["parameters"]["properties"]["worker"]["enum"] = list(
            self.workers.keys()
        )
        self.function["parameters"]["properties"]["control_flow_process"][
            "enum"
        ] = list(self.control_flows.keys())
