from api.openai import openai_chat
from core.context import Context

logit_bias = { 
    1102: -100, 
    4717: -100, 
    7664: -100
    }

class Process:
    def __init__(
            self,
            system_init,
            config=None,
            context=True
        ):
        self.context = Context()
        self.messages = []
        self.messages.append({ "role": "system", "content": system_init })
        self.config = {
               "model": "gpt-4-0613",
               "temperature": 1.8,
               "top_p": 0.5,
               "frequency_penalty": 0.2,
               "presence_penalty": 0.2,
               "logit_bias": logit_bias,
               "stream": False,
            }

        if context == True:
            self.context = Context()
    
    def nth_shot(self, message, role="user"):
        self.messages.append({ "role": role, "content": message })

    def functions(self, functions):
        self.functions = functions

    def __call__(self, message, role="user"):
        self.messages.append({ "role": role, "content": message })
        response = openai_chat(self.messages)
        response_data= response['choices'][0]

        # self.context(response_data)
        # self.functions(response_data.message.function_call)
        return response_data.message.content

