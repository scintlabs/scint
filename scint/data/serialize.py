import base64
import json
import asyncio
import ast
import re
import functools

from pydantic import BaseModel

from scint.core.models import Arguments, Embedding, File, Link
from scint.core.models import AssistantMessage
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


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
