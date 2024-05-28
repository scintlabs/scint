import asyncio
import datetime
import os
import uuid

import aiohttp
from kagiapi import KagiClient

from scint.core.models import SystemMessage
from scint.modules.logging import log
from scint.support.utils import encode_image


def make_function_list():
    functions = []
    for name, func in locals().items():
        if callable(func) and hasattr(func, "metadata"):
            instance = func
            functions.append(instance)
    return functions


functions = make_function_list()


async def search_web(query: str):
    search_web.metadata = "search_web"
    kagi = KagiClient(os.environ.get("KAGI_API_KEY"))
    results = kagi.enrich(query=query)
    for result in results["data"]:
        yield SystemMessage(content=f"{result}")


async def search_github_repos(query: str):
    search_github_repos.metadata = "search_github_repos"
    log.info(f"Searching GitHub repositories for: {query}")
    process = await asyncio.create_subprocess_shell(
        f"gh search repos {query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    full_output = output + "\n" + errors if errors else output

    yield SystemMessage(content=f"{full_output}")


async def download_image(image_url):
    download_image.metadata = "download_image"
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                with open("download.png", "wb") as f:
                    image = await response.read()
                    base64_image = encode_image(image)
                    messages = [
                        {
                            "type": "text",
                            "text": "Respond to the user about the image:",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ]
                    yield SystemMessage(content=messages)
            else:
                yield SystemMessage(content="Failed to download image.")


async def load_file(file_path):
    load_file.metadata = "load_file"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            yield SystemMessage(content=f"{content}")

    except (UnicodeDecodeError, FileNotFoundError, PermissionError):
        yield None


async def create_directory_map(path):
    create_directory_map.metadata = "create_directory_map"

    async def load_file(path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                return content
        except Exception as e:
            log.error(f"Error: {e}")

    dmap = {
        "name": os.path.basename(path) if os.path.basename(path) else path,
        "type": "directory",
        "directory": [],
    }

    data_list = []
    index_list = []

    async def traverse_directory(current_path):
        items = []
        for entry in os.scandir(current_path):
            if entry.is_dir(follow_symlinks=False):
                if entry.name in {".git", "__pycache__", ".DS_Store"}:
                    continue
                sub_dir_map, sub_dir_data, sub_dir_index = await traverse_directory(
                    entry.path
                )
                items.append(sub_dir_map)
                data_list.extend(sub_dir_data)
                index_list.extend(sub_dir_index)
            elif entry.is_file():
                if entry.name.endswith((".txt", ".md", ".py", ".json", ".xml")):
                    content = await load_file(entry.path)
                    file_entry = {
                        "name": entry.name,
                        "type": "file",
                        "content": content,
                    }
                    items.append(file_entry)

                    data_obj = {
                        "id": str(uuid.uuid4()),
                        "name": entry.name,
                        "path": entry.path,
                        "created_on": datetime.fromtimestamp(
                            entry.stat().st_ctime
                        ).isoformat(),
                        "last_edited": datetime.fromtimestamp(
                            entry.stat().st_mtime
                        ).isoformat(),
                        "content": content,
                    }
                    data_list.append(data_obj)

                    # Prepare index object
                    index_obj = {
                        "id": data_obj["id"],
                        "name": entry.name,
                        "content": content[:180],
                        "tags": [],
                    }
                    index_list.append(index_obj)

        current_map = {
            "name": os.path.basename(current_path),
            "type": "directory",
            "directory": items,
        }
        return current_map, data_list, index_list

    map, data, index = await traverse_directory(path)
    return map, data, index


async def use_terminal(commands: str):
    use_terminal.metadata = "use_terminal"
    use_terminal.metadata("use_terminal")
    process = await asyncio.create_subprocess_shell(
        commands,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    full_output = output + "\n" + errors if errors else output
    yield SystemMessage(content=full_output)


async def swap_context(context):
    yield SystemMessage(content=f"Switched context to {context}")


async def merge_context(context):
    yield SystemMessage(content=f"Switched context to {context}")


enum = [
    "Module",
    "Module",
    "Module",
    "Module",
    "Module",
    "Module",
    "Module",
    "Module",
    "Module",
]

functions = [
    {
        "name": "swap_context",
        "import_path": "scint.core.lib.functions",
        "categories": ["core"],
        "description": "This function allows you to swap the messages loaded in your context window for ones that may be more relevant to the conversation.",
        "parameters": {
            "type": "object",
            "properties": {
                "context": {
                    "type": "string",
                    "description": "The name of the context to switch to.",
                    "enum": [*enum],
                }
            },
            "required": ["context"],
        },
        "keywords": [
            "context",
            "switch",
            "change",
            "context switch",
            "context change",
            "enhance memory",
            "contextual",
        ],
    },
    {
        "name": "swap_context",
        "import_path": "scint.core.lib.functions",
        "categories": ["core"],
        "description": "This function allows you to swap the messages loaded in your context window for ones that may be more relevant to the conversation.",
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
        "keywords": [
            "context",
            "switch",
            "change",
            "context switch",
            "context change",
            "enhance memory",
            "contextual",
        ],
    },
    {
        "name": "download_image",
        "import_path": "scint.core.lib.functions",
        "categories": ["initial"],
        "description": "Use this function to view images when the user requests feedback on an image in link format.",
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
        "keywords": ["image", "view", "link", "image url", "image viewer"],
    },
    {
        "name": "create_directory_map",
        "import_path": "scint.core.lib.functions",
        "categories": ["initial"],
        "description": "Recursively maps the directory structure and file contents of a given path, returning a dictionary representation. Used for generating a hierarchical representation of a directory tree with file contents.",
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
        "keywords": [
            "directory",
            "dir",
            "mapping",
            "recursive",
            "files",
            "finder",
            "file contents",
        ],
    },
    {
        "name": "load_file_chunks",
        "categories": ["initial"],
        "import_path": "scint.core.lib.functions",
        "description": "Reads a file object in specified chunk sizes. Useful for processing large files incrementally to avoid memory constraints.",
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
        "keywords": [
            "read file",
            "chunking",
            "files",
            "process files",
            "load data",
        ],
    },
    {
        "name": "load_file",
        "categories": ["initial"],
        "import_path": "scint.core.lib.functions",
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
        "keywords": ["read file", "open file", "load file", "file", "text content"],
    },
    {
        "name": "use_terminal",
        "categories": ["initial"],
        "import_path": "scint.core.lib.functions",
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
        "keywords": [
            "terminal",
            "shell",
            "macos",
            "cli",
            "command",
            "command line",
            "subprocess",
        ],
    },
    {
        "name": "recursive_getattr",
        "categories": ["initial"],
        "import_path": "scint.core.lib.functions",
        "description": "Recursively retrieves the value of a specified attribute from an object, supporting dot notation for nested attributes.",
        "parameters": {
            "type": "object",
            "properties": {
                "obj": {
                    "type": "object",
                    "description": "The object to retrieve the attribute from.",
                },
                "attr": {
                    "type": "string",
                    "description": "The attribute name to retrieve, supporting dot notation for nested attributes.",
                },
            },
            "required": ["obj", "attr"],
        },
        "keywords": [
            "attribute retrieval",
            "recursive",
            "dot notation",
            "dict access",
            "python dictionry",
            "nested attributes",
        ],
    },
    {
        "name": "search_web",
        "categories": ["initial"],
        "import_path": "scint.core.lib.functions",
        "description": "Searches the web using the specified query and yields enriched results.",
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
        "keywords": ["web search", "search", "enrich results", "query"],
    },
    {
        "name": "search_github_repos",
        "categories": ["initial"],
        "import_path": "scint.core.lib.functions",
        "description": "Searches GitHub repositories using the specified query and yields the search results.",
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
        "keywords": ["GitHub", "repository search", "search", "query", "repos"],
    },
]
