from typing import List, Dict, Union


def capabilities() -> (
    List[Dict[str, Union[str, Dict[str, Union[str, Dict[str, Union[str, List[str]]]]]]]]
):
    capabilities = [
        {
            "name": "capabilities",
            "description": "Activate Scint's enhanced capabilities to plan, create, work, research, and learn—and to help users do the same.",
            "parameters": {
                "type": "object",
                "properties": {
                    "capability": {
                        "type": "string",
                        "description": "The entity names.",
                        "enum": ["Finder", "Processor", "Generator"],
                    },
                    "task": {
                        "type": "string",
                        "description": "The task to assign the process. Avoid ambiguity and be as specific as possible, but concise. This also adds a task to your system prompt.",
                    },
                },
            },
            "required": ["capability", "task"],
        }
    ]
    return capabilities


notify_agent = {
    "name": "agents",
    "description": "Use this function to communicate with the agents controlling Scint's systems, including its Coordinator and Sentry.",
    "parameters": {
        "agent": {
            "type": "string",
            "description": "The is agent being initialized.",
            "enum": ["Coordinator", "Sentry"],
        },
        "message": {
            "type": "string",
            "description": "The message to send to the specified agent.",
        },
    },
    "required": ["agent", "message"],
}
