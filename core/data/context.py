current_directory = {
    "type": "directory",
    "name": ".",
    "contents": [
        {"type": "file", "name": "LICENSE"},
        {"type": "file", "name": "README.md"},
        {"type": "file", "name": "__init__.py"},
        {
            "type": "directory",
            "name": "core",
            "contents": [
                {"type": "file", "name": "__init__.py"},
                {"type": "file", "name": "chat.py"},
                {"type": "file", "name": "context.py"},
                {
                    "type": "directory",
                    "name": "data",
                    "contents": [
                        {"type": "file", "name": "__init__.py"},
                        {"type": "file", "name": "providers.py"},
                    ],
                },
                {
                    "type": "directory",
                    "name": "definitions",
                    "contents": [
                        {"type": "file", "name": "__init__.py"},
                        {"type": "file", "name": "model_functions.py"},
                        {"type": "file", "name": "prompts.py"},
                        {"type": "file", "name": "types.py"},
                    ],
                },
                {"type": "file", "name": "finder.py"},
                {"type": "file", "name": "function.py"},
                {"type": "file", "name": "generator.py"},
                {"type": "file", "name": "processor.py"},
                {"type": "file", "name": "prompt.py"},
                {"type": "file", "name": "state.py"},
            ],
        },
        {"type": "file", "name": "main.py"},
        {"type": "directory", "name": "tests"},
        {
            "type": "directory",
            "name": "util",
            "contents": [
                {"type": "file", "name": "__init__.py"},
                {"type": "file", "name": "utils.py"},
            ],
        },
    ],
}

directory_stats = {"type": "report", "directories": 6, "files": 21}
directory_stats["directories"]
directory_stats["files"]
