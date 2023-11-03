import json
import asyncio
import importlib
from typing import Dict, List, Any

from core.agents import Actor
from services.openai import completion
from services.logger import log
from core.memory import ContextController


class Worker(Actor):
    def __init__(self, name, system_init, function, config):
        # log.info(f"Worker: initializing {name}.")

        self.name: str = name
        self.system_init: Dict[str, str] = system_init
        self.context: List[Dict[str, str]] = [self.system_init]
        self.function: Dict[str, Any] = function
        self.function_call: Dict[str, str] = {"name": function.get("name")}
        self.config: Dict[str, Any] = config
        self.context_controller = ContextController(4)

    async def process_request(self, request) -> Dict[str, str] | None:
        log.info(f"Worker: processing request: {request}")

        state = await self.get_state()
        response = await completion(**state)
        function_call = response.get("function_call")

        if function_call is not None:
            try:
                async for chunk in self.call_function(response):
                    yield chunk
            except Exception as e:
                log.error(f"Error coordinating worker: {e}")
                yield {"error": f"Error coordinating worker: {e}"}

        else:
            yield response

    async def call_function(self, response):
        log.info("Worker: evaluating function call.")

        function_call = response.get("function_call")
        function_name = function_call.get("name")
        function_args = function_call.get("arguments")

        # Ensure function_args is a dictionary
        if isinstance(function_args, str):
            function_args = json.loads(function_args)

        if function_name.strip() == self.function.get("name"):
            module_name = f"handlers.{function_name}"
            try:
                module = importlib.import_module(module_name)
                method_to_call = getattr(module, function_name, None)

                if method_to_call:
                    result = await method_to_call(**function_args)
                    yield result

                else:
                    log.error(f"Function {function_name} not found in {module_name}.")
                    yield {
                        "error": f"Function {function_name} not found in {module_name}."
                    }

            except ImportError as e:
                log.error(f"Module {module_name} could not be imported: {e}")
                yield {"error": f"Module {module_name} could not be imported: {e}"}
            except Exception as e:
                log.error(f"Error during function call: {e}")
                yield {"error": f"Error during function call: {e}"}
        else:
            log.error(
                f"Function name mismatch. Expected: {self.function.get('name')}, Received: {function_name}"
            )
            yield {
                "error": f"Function name mismatch. Expected: {self.function.get('name')}, Received: {function_name}"
            }
