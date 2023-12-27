import json

from scint.core.context import ContextController
from scint.core.messages import Message
from scint.core.persona import Persona
from scint.core.processor import Processor
from scint.services import openai
from scint.services.logger import log


class Assistant:
    def __init__(self):
        self.name = "Assistant"
        log.info(f"Initializing {self.name} ...")

        self.context_controller = ContextController()
        self.persona = Persona()
        self.processor = Processor()

        log.info(f"{self.name} is ready.")

    async def generate_response(self, message):
        log.info(f"{self.name}: generating response.")

        self.context_controller.add_message(message)
        persona_state = self.persona.get_state()

        for message in self.context_controller.get_global_context():
            persona_state["messages"].append(message.data_dump())

        try:
            response = await openai.completion(**persona_state)
            content = response.get("content")
            tool_calls = response.get("tool_calls")

            if content is not None:
                reply = Message("assistant", content, self.__class__.__name__)
                self.context_controller.add_message(reply)
                yield reply

            if tool_calls is not None:
                log.info(tool_calls)
                self.parse_tool_call(tool_calls)

        except Exception as e:
            log.info(f"{self.name}: {e}.")

    async def parse_tool_call(self, tool_calls):
        log.info(f"{self.name}: parsing tool call.")

        try:
            for tool_call in tool_calls:
                func = tool_call.get("function")
                name = func.get("name")
                arguments = func.get("arguments")
                func_args = json.loads(arguments)

                for tool in self.tools:
                    if tool.name == name:
                        tool_eval = await tool.evaluate(
                            name, self.__class__.__name__, **func_args
                        )
                        yield tool_eval

        except Exception as e:
            log.error(f"{self.name}: Error in parsing tool call - {e}")


assistant = Assistant()
