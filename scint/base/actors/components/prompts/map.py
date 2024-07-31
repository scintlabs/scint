directory = {
    "name": "map",
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
}

file = {
    "name": "file",
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
}
