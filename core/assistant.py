from core.providers.openai import api_call
from core.functions import functions
from core.context import Context


class Assistant:
    def __init__(self, name):
        self.name = name
        self.functions = functions
        self.context = Context(name)

    def chat(self, message):
        self.messages = self.context.state.events["messages"]
        self.messages.append({"role": "user", "content": message})
        response = api_call(self.messages, self.functions)
        data = response["choices"][0]["message"]

        if "function_call" in data and data["function_call"] is not None:
            function = data["function_call"]
            self.eval_function(function)

        if "content" in data and data["content"] is not None:
            assistant_message = data["content"]
            self.messages.append({"role": "assistant", "content": assistant_message})
            return assistant_message

    def eval_function(self, function):
        function_name = function["name"]
        function_arguments = function["arguments"]
        if function_name == "python_code":
            data = json.loads(function_arguments)
            code = data["code"]
            try:
                result = exec(code)
                self.messages.append({"role": "system", "content": result})
            except Exception as e:
                print(f"{e}")

            if data.get("function_call"):
                self.eval_function(data)

    def save(self):
        self.context.state.save_filestore()
