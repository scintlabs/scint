import json
from core.providers.openai import gpt
from core.state import State
from core.context import Context
from core.environment import Environment
from core.functions import functions


functions = functions


class Collaborator:
    def __init__(self):
        self.state = State()
        self.env = Environment()
        self.context = Context()
        self.functions = functions
        self.messages = []

    def chat(self, user_message):
        self.core = self.state.core()
        self.messages.append({"role": "system", "content": self.core})
        self.messages.append({"role": "system", "content": self.env.loadout})
        self.messages.append({"role": "user", "content": user_message})
        response = gpt(self.messages, self.functions)

        if (
            "function_call" in response["choices"][0]["message"]
            and response["choices"][0]["message"]["function_call"] is not None
        ):
            function = response["choices"][0]["message"]["function_call"]
        if (
            "content" in response["choices"][0]["message"]
            and response["choices"][0]["message"]["content"] is not None
        ):
            assistant_message = response["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": assistant_message})
            function_return = self.eval_function(function)
            return assistant_message, function_return

    def eval_function(self, function):
        function_name = function["name"]
        function_arguments = function["arguments"]
        data = json.loads(function_arguments)
        content = data["content"]
        return content

        if data.get("function_call"):
            self.eval_function(data)
