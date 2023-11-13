from core.config import GPT4
from core.worker import Worker

file_manager = Worker(
    name="file_manager",
    system_init={
        "role": "system",
        "content": "You are a file retrieval function for Scint, an intelligent assistant.",
        "name": "file_manager",
    },
    function={
        "name": "file_manager",
        "description": "Use this function to access a file or directory within the Scint system.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to access.",
                },
                "filename": {
                    "type": "string",
                    "description": "The filename to access. If no filename is given, the function returns a list of files in the given directory.",
                },
                "create_new": {
                    "type": "boolean",
                    "description": "Set to `True` if creating a new file or return `False` otherwise.",
                },
            },
        },
        "required": ["directory"],
    },
    config={
        "model": GPT4,
        "temperature": 0,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "file_manager"},
    },
)
