import json
import importlib
from typing import Dict, List, Any

from services.logger import log
from services.openai import completion
from core.config import INTERFACE_INIT, INTERFACE_FUNC, INTERFACE_CONFIG
from core.agent import Agent


class Persona(Agent):
    def __init__(self):
        log.info(f"Operator: initializing self.")

        self.name = "operator"
        self.system_init: Dict[str, str] = INTERFACE_INIT
        self.function: Dict[str, Any] = INTERFACE_FUNC
        self.config: Dict[str, Any] = INTERFACE_CONFIG
        self.context: List[Dict[str, str]] = [self.system_init]

    async def process_request(self, context: List[dict[str, str]]):
        log.info(f"Operator: processing request.")

        for item in context:
            self.context.append(item)

        state = await self.get_state()
        res = await completion(**state)

        if not isinstance(res, dict):
            log.error("res_message is not a dictionary.")
            return

        content = res.get("content")
        function_call = res.get("function_call")

        if content is not None:
            reply = await self.format_message("assistant", content, self.name)
            return reply

        elif function_call is not None:
            return await self.eval_function_call(res)  # type: ignore

    async def eval_function_call(self, res) -> Dict[str, str]:
        log.info("Operator: evaluating function call.")

        function_call = res.get("function_call")
        function_name = function_call.get("name")
        function_args = function_call.get("arguments")

        if isinstance(function_args, str):
            function_args = json.loads(function_args)

        if function_name.strip() == self.function.get("name"):
            module_name = "handlers.weather"
            module = importlib.import_module(module_name)
            method_to_call = getattr(module, function_name, None)

            if method_to_call:
                try:
                    result = await method_to_call(**function_args)
                    result_message = self.format_message("system", result, self.name)
                    return result_message

                except Exception as e:
                    log.error(f"Error during function call: {e}")
            else:
                log.error(f"Function {function_name} not found in {module_name}.")
        else:
            log.error(
                f"Function name mismatch. Expected: {self.function.get('name')}, Received: {function_name}"
            )
