import json

from scint.core.processes import Process
from scint.core.messages import SystemMessage, UserMessage
from scint.core.tools import Tool, Tools
from scint.services.openai import tool_completion
from scint.services.logger import log


class WriteProse(Tool):
    name = "WriteProse"
    description = "Generates prose based on a given prompt."
    props = {
        "prompt": {
            "type": "string",
            "description": "The prompt to generate prose from.",
        },
    }
    required = ["prompt"]

    async def execute_action(self, prompt: str) -> SystemMessage:
        try:
            prose = await tool_completion("openai", "generate_text", {"prompt": prompt})
            return SystemMessage(prose, self.__class__.__name__)

        except Exception as e:
            log.error(f"Error generating prose: {e}")
            return SystemMessage("Unable to generate prose.", self.__class__.__name__)


class CheckGrammar(Tool):
    name = "search_web"
    description = "Use this function to check content for grammar. "
    props = {
        "corrections": {
            "type": "string",
            "description": "Use this parameter to return the corrected text.",
        },
    }
    required = ["query"]

    async def execute_action(self, prompt: str) -> SystemMessage:
        try:
            prose = await tool_completion("openai", "generate_text", {"prompt": prompt})
            return SystemMessage(prose, self.__class__.__name__)

        except Exception as e:
            log.error(f"Error generating prose: {e}")
            return SystemMessage("Unable to generate prose.", self.__class__.__name__)


class Composition(Process):
    identity = "You are a content generation process for an intelligent assistant, capable of producing creative and technical content based on user inputs."
    instructions = "Leverage language models to generate high-quality, relevant content in response to user prompts. Ensure content is coherent, contextually appropriate, and adheres to any specified guidelines or constraints."
    tools = Tools()
    tools.add(WriteProse())

    async def call(self, message: UserMessage):
        self.context.add(message)
        state = self.get_state()
        log.info(state)

        try:
            async for completions in tool_completion(**state):
                for tool_call in completions:
                    function = tool_call.get("function")
                    tool_name = function.get("name")
                    func_args = json.loads(function.get("arguments", "{}"))
                    tool_instance = self.tools.get(tool_name)

                    try:
                        if tool_instance is not None:
                            response = await tool_instance.execute_action(**func_args)
                            log.info(response.data_dump())
                            yield response

                    except Exception as e:
                        log.error(f"{self.__class__.__name__}: {e}")
                        raise

        except Exception as e:
            log.error(f"{self.__class__.__name__}: {e}")
            raise
