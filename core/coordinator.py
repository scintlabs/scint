import json
from typing import List, Dict, Any

from services.logger import log
from services.openai import completion
from core.config import GPT4
from core.message import Message
from core.interface import ChatInterface
from core.worker import Worker
from core.agent import Agent

coordinator_init = {
    "role": "system",
    "content": "You are the Coordinator module for Scint, an intelligent assistant. You're responsibile for classifying all incoming requests and assigning them to the appropriate worker.",
    "name": "Coordinator",
}

coordinator_func = {
    "name": "coordinate",
    "description": "Define the task and assign it to the appropriate worker.",
    "parameters": {
        "type": "object",
        "properties": {
            "worker": {
                "type": "string",
                "description": "Select the appropriate worker based on the task and request.",
                "enum": ["chat", "get_weather"],
            },
            "task": {
                "type": "string",
                "description": "Based on the request, define the task the worker needs to complete. Avoid ambiguity and be specific.",
            },
            "classification": {
                "type": "string",
                "description": "Classify the type of request being made.",
                "enum": ["general_discussion", "information_request"],
            },
        },
    },
    "required": ["worker", "task", "classification"],
}

coordinator_config = {
    "model": GPT4,
    "temperature": 0,
    "top_p": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "function_call": {"name": "coordinate"},
}


class Coordinator(Agent):
    def __init__(self):
        log.info(f"Initializing coordinator.")

        self.name = "coordinator"
        self.system_init: Dict[str, str] = coordinator_init
        self.messages: List[Dict[str, str]] = [self.system_init]
        self.function: Dict[str, Any] = coordinator_func
        self.config: Dict[str, Any] = coordinator_config
        self.interface = ChatInterface()
        self.workers: Dict[str, Worker] = {}

    async def process_request(self, request):
        log.info(f"Processing request: {request.message}")

        self.request: Message = request
        self.messages = [self.system_init]
        self.messages.append(self.request.message)
        state = await self.state()
        res = await completion(**state)
        res_message = res["choices"][0].get("message")  # type: ignore
        function_call = res_message.get("function_call")

        if function_call is not None:
            response = await self.eval_function_call(res_message, request)
            return response

    async def eval_function_call(self, res_message, original_request):
        log.info("Evaluating coordinator function call.")

        function_call = res_message.get("function_call")
        function_name = function_call.get("name")
        function_args = function_call.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == "coordinate":
            worker = function_args.get("worker")
            task = function_args.get("task")
            classification = function_args.get("classification")

            try:
                log.info(f"Assigning {classification} task to {worker}: {task}")

                if worker.strip() == "chat":
                    req = original_request
                    res = await self.interface.process_request(req)
                    return res

                else:
                    worker_name = worker.strip()
                    task_message = {
                        "role": "system",
                        "content": task,
                        "name": "Coordinator",
                    }
                    req = Message("Coordinator", worker_name, task_message)
                    worker_res = await self.workers[worker_name].process_request(req)
                    final_res = await self.interface.process_request(worker_res)
                    return final_res

            except Exception as e:
                log.error(f"Error coordinating worker: {e}")
        else:
            log.error("Function name is not 'coordinate'.")

    def add_worker(self, worker):
        log.info(f"Adding worker to coordinator: {worker.name}.")

        self.workers[worker.name] = worker
