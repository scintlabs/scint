import json
import importlib
from datetime import datetime
from typing import Dict, Any

from core.agents import Agent, AgentMatrix, AgentFunction
from core.memory import ContextController, Message
from core.config import WORKER_CONFIG
from services.openai import generate_completion
from services.logger import log


FUNCTION_TO_MODULE_MAP = {
    "search_web": "web",
    "load_website": "web",
    "file_manager": "filesystem",
    "get_weather": "api",
}


class Worker(Agent):
    def __init__(self, name, purpose, description, params, req):
        super().__init__(WORKER_CONFIG)

        self.matrix = AgentMatrix(name=name, personality=purpose)
        self.function = AgentFunction(
            name=name, desc=description, params=params, req=req
        )
        self.context = ContextController(2, 4)

    async def process_request(self, request):
        log.info(f"Worker: processing request.")

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
            async for chunk in self.eval_function(response_function):
                self.context.add_message(chunk)
                yield chunk

    async def eval_function(self, response_function):
        log.info(f"Worker: evaluating function call.")

        function_name = response_function.get("name")
        function_args = response_function.get("arguments")
        function_args = json.loads(function_args)

        if function_name.strip() == self.function.name:
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
