routines = {
    "queues": ["clarify", "develop", "evaluate", "refine"],
    "states": {
        "CLARIFY": "Clarifying requirements.",
        "DEVELOP": "Developing requirements-based processes.",
        "EVALUATE": "Evaluating processes.",
        "REFINE": "Refining results.",
    },
}

subroutines = {
    "queues": ["functions", "chains"],
    "states": {
        "SPAWN": "Spawning executor.",
        "EXECUTE": "Preparing execution parameters.",
        "FUNCTION": "Executing function.",
        "CALLBACK": "Executing callback.",
        "PROCESS": "Executing process.",
        "FAIL": "Failed.",
        "RETRY": "Retrying.",
        "SUCCESS": "Success.",
        "TERMINATE": "Terminating executor.",
    },
}
