import json
import importlib
from typing import Dict, Any

from core.agents import Actor
from core.config import DEFAULT_CONFIG, DEFAULT_INIT
from services.openai import completion
from services.logger import log


FUNCTION_TO_MODULE_MAP = {
    "search_web": "web",
    "load_website": "web",
    "file_manager": "filesystem",
    "get_weather": "api",
}


class Worker(Actor):
    def __init__(self, name, function, config=DEFAULT_CONFIG, system_init=DEFAULT_INIT):
        super().__init__(name, config, system_init)
        self.function: Dict[str, Any] = function
        self.function_call: Dict[str, str] = {"name": function.get("name")}

    async def process_request(self, request):
        log.info(f"Worker: processing request.")

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
        log.info(f"Worker: evaluating function call.")

        function_name = response_function.get("name")
        function_args = response_function.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == self.name:
            module_name = FUNCTION_TO_MODULE_MAP.get(function_name)

            if not module_name:
                log.error(f"No module found for function {function_name}.")
                yield

            module_path = f"handlers.{module_name}"

            try:
                module = importlib.import_module(module_path)
                method_to_call = getattr(module, function_name, None)

                if method_to_call:
                    result = await method_to_call(**function_args)
                    yield result

                else:
                    log.error(f"Function {function_name} not found in {module_path}.")

            except ImportError as e:
                log.error(f"Module {module_path} could not be imported: {e}")
                yield

            except Exception as e:
                log.error(f"Error during function call: {e}")
                yield
