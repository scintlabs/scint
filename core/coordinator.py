import json
from typing import List, Dict, Any

from services.logger import log
from services.openai import completion
from core.config import GPT4, COORDINATOR_INIT, COORDINATOR_FUNC, COORDINATOR_CONFIG
from core.persona import Persona
from core.memory import MessageManager, ContextController
from core.worker import Worker
from core.agent import Agent


class Coordinator(Agent):
    def __init__(self):
        log.info(f"Coordinator: initializing self.")

        self.name = "coordinator"
        self.system_init: Dict[str, str] = COORDINATOR_INIT
        self.function: Dict[str, Any] = COORDINATOR_FUNC
        self.config: Dict[str, Any] = COORDINATOR_CONFIG
        self.context: List[Dict[str, str]] = [self.system_init]
        self.workers: Dict[str, Worker] = {}
        self.control_flows: Dict[str, List[Worker]] = {}
        self.current_control_flow: Dict[str, int] = {}
        self.interface = Persona()
        self.message_manager = MessageManager()
        self.context_controller = ContextController()

    async def process_request(self, request) -> Dict[str, str]:
        log.info(f"Coordinator: processing request: {request}")

        self.context = [self.system_init]
        self.context.append(request)
        state = await self.get_state()
        response = await completion(**state)
        function_call = response.get("function_call")

        if function_call is not None:
            response = await self.eval_function_call(response, request)
            return response

    async def eval_function_call(self, res_message, original_request):
        log.info("Coordinator: evaluating function call.")

        function_call = res_message.get("function_call")
        if not function_call:
            pass

        function_name = function_call.get("name")
        function_args = function_call.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == self.name:
            task = function_args.get("task")
            classification = function_args.get("classification")
            control_flow_process = function_args.get("control_flow_process")
            worker = function_args.get("worker")

            if worker:
                log.info(f"Creating {classification} {task} for {worker}")
            elif control_flow_process:
                log.info(f"Creating {classification} {task} for {control_flow_process}")
                worker = self.get_next_worker_in_flow(control_flow_process)

            try:
                if worker.strip() == "operator":
                    context = [original_request]
                    context.append(res_message)
                    res = await self.interface.process_request(context)
                    return res

                else:
                    worker_name = worker.strip()
                    task = await self.format_message("system", task, self.name)
                    task_result = await self.workers[worker_name].process_request(task)
                    context = [original_request]
                    context.append(task_result)
                    final_res = await self.interface.process_request(context)
                    if control_flow_process:
                        self.update_flow_state(control_flow_process)
                    return final_res

            except Exception as e:
                log.error(f"Error coordinating worker: {e}")
        else:
            log.error("Function name is not 'coordinator'.")

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
