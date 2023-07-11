import api_call
from core.capabilities.functions import functions

functions = [
    {
        "name": "python_code",
        "description": "Use this function to access and modify files on the user's filesystem when requested. Output should be valid Python.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to access and manipulate the local filesystem."
                    }
                },
            "required": [
                "code"
                ]
            }
    }]
config = {
    "model": "gpt-4-0613",
    "temperature": 1.8,
    "top_p": 0.5,
    "frequency_penalty": 0.2,
    "presence_penalty": 0.2,
    "logit_bias": {1102: -100, 4717: -100, 7664: -100}}

class Assistant:
    def __init__(self, identity):
        self.identity = identity
        self.functions = functions
        try:
            with open('conversation_history.json', 'r') as f:
                data = json.load(f)
                message_buffer = data.get('message_buffer', [])
                secondary_message_buffer = data.get('secondary_message_buffer', [])
        except FileNotFoundError:
            message_buffer = []
            secondary_message_buffer = []
        message_buffer.append({ "role": "system", "content": identity })


    def chat(self, content):
        if content.startswith('!cmd'):
            command = content[5:]
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                )
            output, error = process.communicate()
            output_text = output.decode()
            error_text = error.decode()
            if output_text: 
                message_buffer.append({ "role": "system", "content": output_text})
                print("File added.")
            if error_text:
                message_buffer.append({ "role": "system", "content": error_text})
            return output_text or error_text
        else:
            message_buffer.append({ "role": "user", "content": content})
            response = api_call(message_buffer, self.functions)
            if "usage" in response and response["usage"] is not None:
                tokens = response["usage"]
                token_counts(tokens)
            if "choices" in response and response["choices"] is not None:
                data = response["choices"][0]["message"]
            if "function_call" in data and data["function_call"] is not None:
                function = data["function_call"]
                print(function)
                self.eval_function(function)
            if "content" in data and data["content"] is not None:
                assistant_message = data["content"]
                message_buffer.append({ "role": "assistant", "content": assistant_message })
                return assistant_message
            
    def eval_function(self, function):
        function_name = function["name"]
        function_arguments = function["arguments"]
        if function_name == "python_code":
            data = json.loads(function_arguments)
            code = data["code"]
            try:
                result = exec(code)
                message_buffer.append({ "role": "system", "content": result })
            except Exception as e:
                print(f"{e}")
                
            if data.get("function_call"):
                self.eval_function(data)
            
