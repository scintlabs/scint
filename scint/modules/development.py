from scint.core.processes import Process
from scint.core.messages import SystemMessage
from scint.core.tools import Tool, Tools
from scint.services.openai import tool_completion
from scint.services.logger import log


from scint.core.tools import Tool
from scint.services.logger import log


class LintCode(Tool):
    name = "lint_code"
    description = "Lints and analyzes code for programming and stylistic errors."
    props = {
        "code": {
            "type": "string",
            "description": "The code to lint.",
        },
        "language": {
            "type": "string",
            "description": "Programming language of the code.",
        },
    }
    required = ["code", "language"]

    async def execute_action(self, code: str, language: str) -> SystemMessage:
        linting_result = f"Linting results for {language} code: {code}"

        try:
            return SystemMessage(linting_result, self.__class__.__name__)

        except Exception as e:
            log.error(f"Error linting code: {e}")
            return SystemMessage("Unable to lint the code.", self.__class__.__name__)


class WriteCode(Tool):
    name = "Coder"
    description = "Generates code based on a given prompt or specification."
    props = {
        "prompt": {
            "type": "string",
            "description": "The prompt or specification for code generation.",
        },
    }
    required = ["prompt"]

    async def execute_action(self, prompt: str) -> SystemMessage:
        try:
            code = await tool_completion("openai", "generate_code", {"prompt": prompt})
            return SystemMessage(code, self.__class__.__name__)
        except Exception as e:
            log.error(f"Error generating code: {e}")
            return SystemMessage("Unable to generate code.", self.__class__.__name__)


class Development(Process):
    identity = "You are a content generation process for an intelligent assistant, capable of producing creative and technical content based on user inputs."
    instructions = "Leverage language models to generate high-quality, relevant content in response to user prompts. Ensure content is coherent, contextually appropriate, and adheres to any specified guidelines or constraints."
    tools = Tools()
    tools.add(WriteCode())
