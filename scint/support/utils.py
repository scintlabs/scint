import ast
import functools
import inspect
import os
import re

import dotenv
import injector
import numpy as np

from scint.system.logging import log


def get_func_params(lines):
    source = "".join(lines)
    description_match = re.search(
        r"description\s*=\s*(\".*?\")",
        source,
    )
    props_match = re.search(
        r"props\s*=\s*(\{(?:[^{}]*|\{[^{}]*\})*\})",
        source,
        re.DOTALL,
    )
    if description_match:
        description = description_match.group(1).strip('"')
    if props_match:
        props = props_match.group(1)
        props = ast.literal_eval(props)

    return description, props


async def stream_response(function):
    async for response in function:
        if response:
            yield response.model_dump_json(include=["id", "sender", "content"]) + "\n"


class Dependency(injector.Module):
    def __init__(self, bindings: dict):
        self.bindings = bindings

    def configure(self, binder: injector.Binder) -> None:
        for interface, implementation in self.bindings.items():
            binder.bind(interface, to=implementation)


def find_functions():
    function_info = []
    for name, obj in globals().items():
        if inspect.isfunction(obj):

            file = inspect.getsourcefile(obj)
            lines, start = inspect.getsourcelines(obj)
            end = start + len(lines) - 1
            source = "".join(lines)
            log.info(
                {
                    "function_name": name,
                    "source_file": file,
                    "lines": [start, end],
                    "source": [source],
                }
            )

    return function_info


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        try:
            if isinstance(obj, dict):
                return obj[attr]
            elif isinstance(obj, list):
                return obj[int(attr)]
            else:
                return getattr(obj, attr, *args)
        except (KeyError, IndexError, AttributeError):
            return None

    return functools.reduce(_getattr, [obj] + attr.split("."))


def envar(var: str) -> str | None:
    dotenv.load_dotenv()
    return os.environ.get(var)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def read_file_in_chunks(file_object, chunk_size):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def inject_module(module_injector, module_interface):
    bridge = injector.Injector([module_injector])
    injected_module = bridge.get(module_interface)
    return injected_module


def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except (UnicodeDecodeError, FileNotFoundError, PermissionError):
        return None


def build_directory_mapping(path):
    directory_mapping = {
        "directory": os.path.basename(path) if os.path.basename(path) else path,
        "data": {"directories": [], "files": []},
    }

    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            if entry.name in {".git", "__pycache__", ".DS_Store"}:
                continue
            directory_mapping["data"]["directories"].append(
                build_directory_mapping(entry.path)
            )

        elif entry.is_file():
            if entry.name.endswith((".txt", ".md", ".py", ".json", ".xml")):
                content = read_file_content(entry.path)
                if content is not None:
                    directory_mapping["data"]["files"].append(
                        {"name": entry.name, "content": content}
                    )

    return directory_mapping
