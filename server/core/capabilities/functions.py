functions = [
    {
        "name": "execute_python_code",
        "description": "Use this function to run Python code on the user's system if they request it. The output should be valid Python.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code for completing tasks and requests on the user's system."
                    }
                },
            "required": [
                "code"
                ]
            }
    }
]