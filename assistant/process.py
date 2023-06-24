import json
from .api.openai import openai_chat
from .context import Context

logit_bias = {1102: -100, 4717: -100, 7664: -100}


class Process:
    """main process"""

    def __init__(self, system_init, functions=None, config=None, context=True):
        self.context = Context()
        self.messages = []
        self.messages.append({"role": "system", "content": system_init})
        self.functions = functions
        self.config = config
        self.config = {  # fix the config parameter
            "model": "gpt-4-0613",
            "temperature": 1.8,
            "top_p": 0.5,
            "frequency_penalty": 0.2,
            "presence_penalty": 0.2,
            "logit_bias": logit_bias,
            "stream": False,
        }

    def nth_shot(self, message, role="user"):
        self.messages.append({"role": role, "content": message})

    def eval_function(self, function):  # move out of process class?
        self.function_call = function["function_call"]
        self.function_name = self.function_call["name"]
        self.function_arguments = self.function_call["arguments"]

        if self.function_name == "execute_python_code":
            data = json.loads(self.function_arguments)
            self.code = data["code"]
            print(self.code)
            try:
                exec(self.code)
            except Exception as e:
                print(f"{e}")

    def __call__(self, message, role="user"):
        self.messages.append({"role": role, "content": message})
        response = openai_chat(self.messages, self.functions)
        data = response["choices"][0]["message"]
        self.messages.append(data)
        usage = response["usage"]["total_tokens"]

        if data.get("function_call"):
            self.eval_function(data)

        if data["content"] == None:
            return "Processing request."
        else:
            return data["content"]
