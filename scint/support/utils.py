import ast
import asyncio
import base64
import functools
import hashlib
import inspect
import json
import os
import re

from types import LambdaType
from typing import Any, Coroutine, Final
import dotenv
import numpy as np
from pydantic import BaseModel

from scint.support.logging import log


def hash_object(file_path):
    if os.path.getsize(file_path) > 1e6:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
    with open(file_path, "rb") as f:
        bytes = f.read()
        readable_hash = hashlib.sha256(bytes).hexdigest()
    return readable_hash


def dictorial(data, attr):
    def rgetattr(obj, attr):
        def _getattr(obj, attr):
            try:
                if isinstance(obj, dict):
                    return obj[attr]
                if isinstance(obj, list):
                    return obj[int(attr)]
                return getattr(obj, attr)
            except (KeyError, IndexError, AttributeError, ValueError):
                return None

        return functools.reduce(_getattr, [obj] + attr.split("."))

    try:
        result = rgetattr(data, attr)
        if result is not None:
            return result
        if isinstance(data, dict) and attr in data:
            return data[attr]
        # if isinstance(data, BaseModel):
        #     try:
        #         return data.model_dump().get(attr)
        #     except AttributeError:
        #         pass
        if isinstance(data, str):
            try:
                json_data = json.loads(data)
                if attr in json_data:
                    return json_data.get(attr)
            except json.JSONDecodeError:
                pass
    except (KeyError, IndexError, AttributeError):
        pass
    return None


def keyfob(data, attr):
    def search_nested(obj, attr):
        if isinstance(obj, dict):
            if attr in obj:
                return obj[attr]
            for key, value in obj.items():
                result = search_nested(value, attr)
                if result is not None:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = search_nested(item, attr)
                if result is not None:
                    return result
        else:
            if hasattr(obj, attr):
                return getattr(obj, attr)
            if isinstance(obj, BaseModel):
                try:
                    return obj.model_dump().get(attr)
                except AttributeError:
                    pass
        return None

    try:
        result = search_nested(data, attr)
        if result is not None:
            return result
        if isinstance(data, dict) and attr in data:
            return data[attr]
        if isinstance(data, BaseModel):
            try:
                return data.model_dump().get(attr)
            except AttributeError:
                pass
        if isinstance(data, str):
            try:
                json_data = json.loads(data)
                if attr in json_data:
                    return json_data.get(attr)
            except json.JSONDecodeError:
                pass
    except (KeyError, IndexError, AttributeError):
        pass
    return None


def get_func_params(lines):
    source = "".join(lines)
    description = None
    props = None
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

    if description and props:
        return description, props

    return None, None


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


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


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


def env(var: str) -> str:
    dotenv.load_dotenv()
    return dotenv.get_key("/Users/kaechle/Developer/scint/scint-python/.env", var)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def read_file_in_chunks(file_object, chunk_size):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


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


def attr_from_source(source, attribute_name):
    pattern = re.compile(
        rf"{attribute_name}\s*=\s*({{(?:[^{{}}]*|{{[^{{}}]*}})*}}|\".*?\")", re.DOTALL
    )
    match = pattern.search(source)

    if match:
        value = match.group(1)
        if value.startswith("{"):
            return ast.literal_eval(value)
        else:
            return value.strip('"')
    return None


def parse_function(function):
    source = inspect.getsource(function)
    description = attr_from_source(source, "description")
    props = attr_from_source(source, "props")
    if props and description:
        return True
    return False


def parse_docstring(docstring, *args):
    return docstring.strip()


async def build_props(self):
    description = ""
    props = {}
    if self.modules:
        for module in self.modules:
            description += f"{module.name}: {module.description}\n\n"

        props["module"] = {
            "type": "string",
            "description": "Select an available module to process the request.",
            "enum": [module.name for module in self.modules],
        }
    if self.relays:
        for relay in self.relays:
            description += f"{relay.name}: {relay.description}\n\n"
        props["relay"] = {
            "type": "string",
            "description": "Select an available relay to process the request.",
            "enum": [relay.name for relay in self.relays],
        }

    return props


def find_runtime_functions():
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


def rgetembedding(struct, embedding, best_match=None, best_similarity=-1):
    struct_embedding = struct.embedding
    similarity = cosine_similarity([embedding], [struct_embedding])[0][0]

    if similarity > best_similarity:
        best_match, best_similarity = struct, similarity

    for nested_struct in struct.structs:
        best_match, best_similarity = rgetembedding(
            nested_struct,
            embedding,
            best_match,
            best_similarity,
        )

    return best_match, best_similarity


waitforit = lambda t: asyncio.sleep(t)  # type: ignore
attrlist = lambda l, t: all(hasattr(i, t) for i in l)  # type: ignore

# rules = lambda c: dictorial(config, f"filetype.{lang}.rules.all.{c}")
waitforit = lambda t: asyncio.sleep(t)  # type: ignore
attrlist = lambda l, t: all(hasattr(i, t) for i in l)  # type: ignore
