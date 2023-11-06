import json
import asyncio
import importlib
from typing import Dict, Any

from core.agents import Actor
from core.config import DEFAULT_CONFIG, DEFAULT_INIT
from services.openai import completion
from services.logger import log
import processing.handlers.web_browsing as web


FUNCTION_TO_MODULE_MAP = {
    "get_links": "web_browsing",
    "load_website": "web_browsing",
    "file_operations": "file_operations",
    "get_weather": "api_access",
}


class Worker(Actor):
    def __init__(self, name, function, config=DEFAULT_CONFIG, system_init=DEFAULT_INIT):
        super().__init__(name, config, system_init)
        self.name: str = name
        self.system_init: Dict[str, str] = system_init
        self.function: Dict[str, Any] = function
        self.function_call: Dict[str, str] = {"name": function.get("name")}
        self.config: Dict[str, Any] = config

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

        if isinstance(function_args, str):
            function_args = json.loads(function_args)

        if function_name.strip() == self.function.get("name"):
            module_name = FUNCTION_TO_MODULE_MAP.get(function_name)

            if not module_name:
                log.error(f"No module found for function {function_name}.")
                return

            module_path = f"processing.handlers.{module_name}"

            try:
                module = importlib.import_module(module_path)
                method_to_call = getattr(module, function_name, None)

                if method_to_call:
                    result = await method_to_call(**function_args)
                    log.info(f"Worker: {result}")
                    yield result

                else:
                    log.error(f"Function {function_name} not found in {module_path}.")

            except ImportError as e:
                log.error(f"Module {module_path} could not be imported: {e}")
                yield {"error": f"Module {module_path} could not be imported: {e}"}

            except Exception as e:
                log.error(f"Error during function call: {e}")
                yield {"error": f"Error during function call: {e}"}

        # else:
        #     log.error(
        #         f"Function name mismatch. Expected: {expected_function_name}, Received: {function_name}"
        #     )
        #     yield {
        #         "error": f"Function name mismatch. Expected: {expected_function_name}, Received: {function_name}"
        #     }
