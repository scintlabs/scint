import json
from core.context import Context
from core.state import State
from core.providers.openai import gpt
from core.capabilities.functions import functions

functions = functions


class Assistant:
    def __init__(self, name):
        self.state = State(name)
        self.identity = self.state.identity_constructor()
        self.functions = functions
        self.context = Context(name)

    def chat(self, user_message):
        self.messages = [{"role": "system", "content": self.identity}]
        self.messages.append({"role": "user", "content": user_message})
        response = gpt(self.messages, self.functions)

        if (
            "function_call" in response["choices"][0]["message"]
            and response["choices"][0]["message"]["function_call"] is not None
        ):
            function = response["choices"][0]["message"]["function_call"]
            self.eval_function(function)

        if (
            "content" in response["choices"][0]["message"]
            and response["choices"][0]["message"]["content"] is not None
        ):
            assistant_message = response["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": assistant_message})
            return assistant_message

    def eval_function(self, function):
        function_name = function["name"]
        function_arguments = function["arguments"]
        data = json.loads(function_arguments)
        code = data["code"]
        try:
            result = exec(code)
            self.messages.append({"role": "system", "content": result})
        except Exception as e:
            print(f"{e}")

        if data.get("function_call"):
            self.eval_function(data)
