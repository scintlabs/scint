instructions = [
    {
        "name": "select_objects",
        "categories": ["advise"],
        "descriptions": [
            "Select context objects to improve unerstanding.",
            "Increase contextual awareness.",
            "Contextualize conversation.",
        ],
        "labels": ["advise", "instructions", "default", "system"],
        "content": "Analyze the provided message or messages to determine which data objects should be loaded into the system's context window to enhance understanding and clarity.",
    }
]

functions = [
    {
        "name": "select_objects",
        "categories": ["advise"],
        "descriptions": [
            "Select context objects to improve unerstanding.",
            "Increase contextual awareness.",
            "Contextualize conversation.",
        ],
        "description": "Use this function to select the appropriate objects to enhance understanding and clarity. Pay close attention to the initial message to improve accuracy.",
        "parameters": {"type": "object", "properties": {}},
    }
]
