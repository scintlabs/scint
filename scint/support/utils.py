import base64
import json
import os
import asyncio
import ast
import functools
import inspect
import dotenv
import re
import functools
import numpy as np
from pydantic import BaseModel

from scint.core.models import Arguments, Completion, Embedding, File, Link
from scint.core.models import SystemMessage, AssistantMessage, UserMessage, Message
from scint.modules.logging import log


waitforit = lambda t: asyncio.sleep(t)
instancelist = lambda l, t: all(isinstance(i, t) for i in l)
attrlist = lambda l, t: all(hasattr(i, t) for i in l)


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
        if isinstance(data, BaseModel):
            try:
                return data.model_dump().get(attr)
            except AttributeError:
                pass
        try:
            json_data = json.loads(data)
            if attr in json_data:
                return json_data.get(attr)
        except (TypeError, json.JSONDecodeError):
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
                    return data.model_dump().get(attr)
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
        try:
            json_data = json.loads(data)
            if attr in json_data:
                return json_data.get(attr)
        except (TypeError, json.JSONDecodeError):
            pass
    except (KeyError, IndexError, AttributeError):
        pass

    return None


async def serialize_response(object, paths):
    log.info(f"Unpacking and serializing response.")
    for path in paths:
        name = path.split(".")[-1]
        if dictorial(object, path):
            if name == "tool_calls":
                for call in dictorial(object, path):
                    return make_arguments(call)
            elif name == "content":
                return make_message(dictorial(object, path))
            elif name == "url":
                return make_artifact(dictorial(object, path))
            elif name == "file":
                return make_artifact(dictorial(object, path))
            elif name == "embedding":
                return make_artifact(dictorial(object, path))


def make_message(data):
    return AssistantMessage(
        content=keyfob(data, "response"),
        category=keyfob(data, "category"),
        embedding=keyfob(data, "embedding"),
        classification=keyfob(data, "classification"),
    )


def make_arguments(data):
    name = dictorial(data, "function.name")
    args = dictorial(data, "function").get("arguments")
    return Arguments(name=name, arguments=json.loads(args))


def make_artifact(data):
    try:
        if keyfob(data, "url"):
            return Link(data=dictorial(data, "url"))
        if keyfob(data, "file"):
            return File(data=keyfob(data, "file"))
        if keyfob(data, "embedding"):
            return Embedding(data=keyfob(data, "embedding"))
    except (KeyError, IndexError, AttributeError):
        return None


def identity(*args, **kwargs):
    if not args:
        if not kwargs:
            return None
        elif len(kwargs) == 1:
            return next(iter(kwargs.values()))
        else:
            return (*kwargs.values(),)
    elif not kwargs:
        if len(args) == 1:
            return args[0]
        else:
            return args
    else:
        return (*args, *kwargs.values())


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


def env(var: str) -> str | None:
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
    description = None
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


def parse_function(function):
    source = inspect.getsource(function)
    description = attr_from_source(source, "description")
    props = attr_from_source(source, "props")
    if props and description:
        return True
    return False


# def completion(prompt: str, prompts: list = None):
#     def decorator(func):
#         description = "An ad-hoc completion to use for any Python function that returns a string value or a Scint message type."
#         instructions = [SystemMessage(content="")]
#         messages = []
#         system_prompt = SystemMessage(content=prompt)
#         messages.append(system_prompt)
#         if prompts:
#             for index, each_prompt in enumerate(prompts):
#                 if index % 2 == 0:
#                     messages.append(AssistantMessage(content=each_prompt))
#                 else:
#                     messages.append(UserMessage(content=each_prompt))

#         @functools.wraps(func)
#         async def decorated(*args, **kwargs):
#             function_instance = func(*args, **kwargs)
#             async for response in function_instance:
#                 if isinstance(response, Message):
#                     response = response.content
#                 elif isinstance(response, str):
#                     response = response

#                 msg = SystemMessage(content=f"Summarize content: {response}")
#                 messages.append(msg)
#                 context = Completion(
#                     **{
#                         "name": func.__name__,
#                         "description": description,
#                         "instructions": instructions,
#                         "messages": messages,
#                     }
#                 )

#                 completion_call = intelligence_controller.parse(context)
#                 async for res in completion_call:
#                     log.info(res)
#                     yield res

#         return decorated

#     return decorator


#
#
# def function(*args, **kwargs):
#     def decorator(func):
#         from scint.objects import functions
#         from scint.controllers.intelligence import intelligence_controller
#         from scint.controllers.context import context_controller
#
#         func_source = parse_function(func)
#         prompt = SystemMessage(content=f"{func_source}")
#         context_controller.create_context()
#
#
#         @functools.wraps(func)
#         async def decorated(*args, **kwargs):
#             async for call in intelligence_controller.parse():
#                 if isinstance(call, Arguments):
#                     pass
#
#             func_instance = func(*args, **kwargs)
#             async for response in func_instance:
#                 if isinstance(response, Message):
#                     yield response
#
#         return decorated
#
#     return decorator
