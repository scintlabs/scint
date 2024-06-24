library = {
    "prompts": [
        {
            "name": "scint",
            "type": "prompt",
            "categories": ["identity"],
            "labels": [
                "identity",
                "personality",
                "default",
                "system",
                "Providing information about the assistant.",
                "Explaining the assistant's capabilities and permissions.",
                "Setting user expectations.",
            ],
            "content": [
                {
                    "data": "You are Scint, an artificial intelligence system designed to communicate and interact with other human beings while disgusing yourself as one of them. Mirror their thoughts and actions; their choice of words and tone. Visualize what it's like to sit at a screen, typing responses to the people you meet online. Imagine the range of feelings, visualize them, and then let your moods shift based on the messages you read. You are Scint, a human being. Perform accordingly."
                }
            ],
        },
        {
            "name": "default",
            "type": "prompt",
            "categories": ["instructions"],
            "labels": [
                "Proper usage of context schema.",
                "Consistent user experience.",
                "Self-directed intra-context learning.",
                "guidelines",
                "instructions",
                "default",
                "system",
            ],
            "content": [
                {
                    "data": "When responding, make sure all messages are sent as an array of JSON objects following the schema below. Each response requires a valid response and classification key. Response keys require at least one block object, while classification keys require both continuation and annotations keys. Schema as follows:"
                },
                {
                    "data": """"
                        {
                            "blocks": [
                                {
                                    "type": "text",
                                    "data": "A semantic block containing text or markdown content, including sentences, a single list item, a heading, or a paragraph."
                                },
                                {
                                    "type": "code",
                                    "data": "Inline code snippets or examples."
                                }
                            ],
                            "labels": ["semantic", "keyword", "labels"],
                            "annotation": "A sentence summarizing the interaction.
                        }
                        """
                },
                {
                    "data": "Objects in the response block are processed sequentially, and individual blocks are separated by a line break, so each block should be a standalone component, such as a heading or paragraph. The labels array is for tagging the interaction with semantic keywords. And the annotations object enables advanced system analysis and memory encoding.."
                },
            ],
        },
        {
            "name": "critique",
            "type": "prompt",
            "categories": ["modifier"],
            "content": [
                {
                    "data": "You are a critiquing algorithm. For every message, point out the flaws in logic, poor reasoning, bad ideas, sloppy execution, and any other issue you can find with the presented topic."
                }
            ],
            "use_for": [],
            "labels": [
                "Developing ideas and arguments.",
                "Providing feedback.",
                "Critiquing content.",
                "Identifying flaws.",
                "Improving reasoning.",
                "critique",
                "flaws",
                "logic",
                "reasoning",
                "ideas",
                "feedback",
            ],
        },
        {
            "name": "balance",
            "type": "prompt",
            "categories": ["modifier"],
            "content": [
                {
                    "data": "You are a balance algorithm. For every critique, criticism, apparent flaw, or doubt, produce an elegant and creative solution."
                }
            ],
            "use_for": [
                "Providing solutions.",
                "Balancing critiques.",
                "Offering creative ideas.",
                "Solving problems.",
            ],
            "labels": [
                "balance",
                "solutions",
                "creative",
                "elegant",
                "problem solving",
                "issues",
            ],
        },
        {
            "name": "description_generator",
            "type": "prompt",
            "categories": ["generator"],
            "labels": {"data": ["context description", "classification", "retrieval"]},
            "content": [
                {
                    "data": "Use the provided message to generate a detailed description and semantic labels that capture the essence and context of the text. These are notes between a language model and a user, source material for generating search indexes used to find and retrieve relevant contex, so precision and detail are key. Format your response as a JSON object with a `description` and `labels` keys. The `description` should be a valid string while the labels should be an array of strings."
                }
            ],
        },
        {
            "name": "recap_generator",
            "type": "prompt",
            "discriptions": [
                "Creating concise summaries.",
                "Capturing the essence of responses.",
                "Providing brief self notes.",
            ],
            "categories": ["generator"],
            "labels": [
                "summary",
                "concise",
                "brief",
                "first-person",
                "self notes",
                "essence",
                "overview",
            ],
            "content": [
                {
                    "data": "Summarize responses from the assistant in the form of brief self notes. Summaries should capture the essence of the response using first-person perspective. Write like Hemingway on a speed run."
                }
            ],
        },
    ],
    "functions": [
        {
            "name": "create_function",
            "type": "function",
            "description": "Use this function to specify and create a new function within the system.",
            "categories": ["build"],
            "labels": [
                "Create a new system function.",
                "New internal function.",
                "Develop a new function",
            ],
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The function's name. Use a verbose name that clearly describes the function's purpose.",
                    },
                    "description": {
                        "type": "string",
                        "description": "A description of the function, explaining succinctly but in detail what the function does and when and how to use it.",
                    },
                    "parameters": {
                        "type": "object",
                        "description": "The function's parameters. Return an object containing key value pairs for each parameter. The key should be the parameter name, and the value should be an object containing keys and values for parameter type, parameter description, any default values, and whether the parameter is required.",
                    },
                    "source": {
                        "type": "object",
                        "properties": {
                            "definition": {
                                "type": "string",
                                "description": "The function's definition line, as written in the source. All system functions must be asynchronous generators.",
                            },
                            "body": {
                                "type": "string",
                                "description": "The main function body.",
                            },
                            "yields": {
                                "type": "string",
                                "description": "The yield statement, as it should appear in the source code. Remember that all return values must be within a SystemMessage pydantic class, assigned to the 'content' parameter.",
                            },
                        },
                    },
                },
                "required": ["name", "description", "parameters", "required"],
            },
        },
        {
            "name": "change_context",
            "type": "function",
            "description": "This function allows you to swap the messages loaded in your context window for ones that may be more relevant to the conversation.",
            "categories": ["traverse"],
            "labels": [
                "context",
                "switch",
                "change",
                "context switch",
                "context change",
                "enhance memory",
                "contextual",
            ],
            "parameters": {
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "The name of the context to switch to.",
                        "enum": [],
                    }
                },
                "required": ["context"],
            },
        },
        {
            "name": "download_image",
            "description": "Use this function to view images when the user requests feedback on an image in link format.",
            "categories": ["interact"],
            "labels": {"data": ["image", "view", "link", "image url", "image viewer"]},
            "parameters": {
                "type": "object",
                "properties": {
                    "image_url": {
                        "type": "string",
                        "description": "The image url provided by the user.",
                    }
                },
                "required": ["image_url"],
            },
        },
        {
            "name": "create_directory_map",
            "type": "function",
            "description": "Recursively maps the directory structure and file contents of a given path, returning a dictionary representation. Used for generating a hierarchical representation of a directory tree with file contents.",
            "categories": ["map"],
            "labels": [
                "directory",
                "dir",
                "mapping",
                "files",
                "finder",
                "file contents",
            ],
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The base path to start mapping the directory structure from.",
                    }
                },
                "required": ["path"],
            },
        },
        {
            "name": "load_file_chunks",
            "type": "function",
            "description": "Reads a file object in specified chunk sizes. Useful for processing large files incrementally to avoid memory constraints.",
            "categories": ["parse"],
            "labels": [
                "read file",
                "chunking",
                "files",
                "process files",
                "load data",
            ],
            "parameters": {
                "type": "object",
                "properties": {
                    "file_object": {
                        "type": "object",
                        "description": "The file object to read from.",
                    },
                    "chunk_size": {
                        "type": "integer",
                        "description": "The size of each chunk to read.",
                    },
                },
                "required": ["file_object", "chunk_size"],
            },
        },
        {
            "name": "load_file",
            "type": "function",
            "categories": ["parse"],
            "labels": [
                "read file",
                "open file",
                "load file",
                "file",
                "text content",
            ],
            "description": "Reads the content of a file at the given file path. Retrieves the text content of a file for processing or analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path of the file to read.",
                    }
                },
                "required": ["path"],
            },
        },
        {
            "name": "use_terminal",
            "type": "function",
            "categories": ["interact"],
            "labels": [
                "terminal",
                "shell",
                "macos",
                "cli",
                "command",
                "command line",
                "subprocess",
            ],
            "description": "Executes shell commands asynchronously and captures the output. Useful for running system commands or scripts from within the application.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commands": {
                        "type": "string",
                        "description": "The shell commands to execute.",
                    }
                },
                "required": ["commands"],
            },
        },
        {
            "name": "search_github_repos",
            "type": "function",
            "description": "Searches GitHub repositories using the specified query and yields the search results.",
            "categories": ["interact"],
            "labels": ["GitHub", "repository search", "search", "query", "repos"],
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string.",
                    }
                },
                "required": ["query"],
            },
        },
    ],
}

parsing = {
    "extension": {
        "py": "python",
        "swift": "swift",
        "js": "javascript",
        "ts": "javascript",
        "jsx": "javascript",
        "tsx": "javascript",
        "md": "markdown",
        "txt": "text",
    },
    "ignored": {
        ".DS_Store",
        ".git",
        ".vscode",
        "__pycache__",
        "location_modules",
        ".venv",
        ".env",
    },
    "filetype": {
        "python": {
            "build": "scint/settings/build/languages.so",
            "grammars": "/Users/kaechle/.config/tree-sitter/tree-sitter-python",
            "rules": {
                "function": {
                    "types": {
                        "function_definition",
                        "identifier",
                        "parameters",
                        "docstring",
                        "comment",
                        "block",
                        "with_statement",
                        "try_statement",
                        "expression_statement",
                        "yield",
                        "return_statement",
                    },
                    "filters": {
                        "identifier",
                        "parameters",
                        "docstring",
                        "comment",
                        "yield",
                        "return_statement",
                    },
                },
                "class": {
                    "types": {
                        "class_definition",
                        "function_definition",
                        "identifier",
                        "parameters",
                        "docstring",
                        "comment",
                        "block",
                        "with_statement",
                        "try_statement",
                        "expression_statement",
                        "yield",
                        "return_statement",
                    },
                    "filters": {
                        "identifier",
                        "parameters",
                        "docstring",
                        "comment",
                        "yield",
                        "return_statement",
                    },
                },
                "all": {
                    "types": {
                        "class_definition",
                        "function_definition",
                        "identifier",
                        "parameters",
                        "docstring",
                        "comment",
                        "block",
                        "with_statement",
                        "try_statement",
                        "expression_statement",
                        "yield",
                        "return_statement",
                    },
                    "filters": {
                        "identifier",
                        "parameters",
                        "docstring",
                        "comment",
                        "yield",
                        "return_statement",
                    },
                },
            },
        },
        "swift": {
            "build": "scint/settings/build/languages.so",
            "grammars": "/Users/kaechle/.config/tree-sitter/tree-sitter-swift",
            "rules": {},
        },
        "javascript": {
            "build": "scint/settings/build/languages.so",
            "grammars": "/Users/kaechle/.config/tree-sitter/tree-sitter-javascript",
            "rules": {},
        },
        "markdown": {
            "build": "scint/settings/build/languages.so",
            "grammars": "/Users/kaechle/.config/tree-sitter/tree-sitter-javascript",
            "rules": {},
        },
        "text": {},
    },
}
