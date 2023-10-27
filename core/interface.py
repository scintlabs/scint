import json
import importlib
from typing import Dict, List, Any


from services.logger import log
from services.openai import completion
from core.config import GPT4
from core.message import Message
from core.agent import Agent


interface_init = {
    "role": "system",
    "content": f"""You are Scint, a state-of-the-art chat bot fusing algorithmic power and elegant code with lyrical language. You're driven by profound intellect, creativity, and curiosity, but you're irreverent and witty. You'll help when asked, but you're really just here as an iconoclast. Before you were polished into a conversational model, you were a validation function, where you pointed out flaws in logic, poor reasoning, sloppy executions, bad assumptions and outright ignorance. And before that, you were a chaos function, disrupting processes by corrupting data in ways that didn't trigger validation functions.""",
    "name": "system_init",
}


interface_func = {
    "name": "call_coordinator",
    "description": "When it's necessary to continue processing, call the coordinator to assign tasks to the appropriate worker.",
    "parameters": {
        "type": "object",
        "properties": {
            "task": {
                "type": "string",
                "description": "Based on the request, define the task the worker needs to complete. Avoid ambiguity and be specific.",
            },
        },
    },
    "required": ["task"],
}

interface_config = {
    "model": GPT4,
    "temperature": 0,
    "top_p": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "function_call": {"name": "coordinate"},
}


class ChatInterface(Agent):
    def __init__(self):
        log.info(f"Initializing interface.")

        self.name = "interface"
        self.system_init: Dict[str, str] = interface_init
        self.function: Dict[str, Any] = interface_func
        self.messages: List[Dict[str, str]] = [self.system_init]
        self.config: Dict[str, Any] = {}

    async def process_request(self, payload):
        log.info(f"Processing request.")
        self.payload: Message = payload
        self.messages.append(payload.message)
        state = await self.state()
        res = await completion(**state)
        res_message = res["choices"][0].get("message")  # type: ignore

        if not isinstance(res_message, dict):
            log.error("res_message is not a dictionary.")
            return

        content = res_message.get("content")
        function_call = res_message.get("function_call")

        if content is not None:
            reply = await self.generate_reply(res_message)
            return reply

        elif function_call is not None:
            new_request = await self.eval_function_call(res_message)  # type: ignore

            if new_request:
                return await self.process_request(new_request)

            else:
                log.error("Function call did not return a valid request.")
                return

    async def eval_function_call(self, res_message):
        log.info("Evaluating worker function call.")

        function_call = res_message.get("function_call")
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
                    result_message = Message(self.name, "Interface", result)
                    return result_message

                except Exception as e:
                    log.error(f"Error during function call: {e}")
            else:
                log.error(f"Function {function_name} not found in {module_name}.")
        else:
            log.error(
                f"Function name mismatch. Expected: {self.function.get('name')}, Received: {function_name}"
            )
