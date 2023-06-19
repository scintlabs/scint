import re
import io
import contextlib
from api.openai import openai_chat
from cogiter.process import Process
from rich.console import Console
from rich.markdown import Markdown

process_config = {
    "model": "gpt-4-0613",
    "temperature": 1.8,
    "top_p": 0.5,
    "frequency_penalty": 0.2,
    "presence_penalty": 0.2,
    "logit_bias": {1102: -100, 4717: -100},
    "stream": False,
}
interface_functions = [
    {
        "name": "execute_python_code",
        "description": "Use this function to run Python code on the user's system on their behalf. The output should be valid Python.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code for completing tasks on the user's system.",
                }
            },
            "required": ["code"],
        },
    }
]


class Interface:
    def __init__(self, identity=None, markdown=True):
        self.console = Console()
        self.output_render = Markdown if markdown else Text
        self.process = Process(identity, interface_functions)
        self.messages = []
        self.messages.append({"role": "system", "content": identity})

    def context(self):
        if context == True:
            self.context = Context()

    def __call__(self, message):
        response = self.process.__call__(message)
        self.console.print(f"[teal]❯❯[/] {response}")
        return
