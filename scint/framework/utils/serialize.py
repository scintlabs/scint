import json
import functools

from pydantic import BaseModel

from scint.framework.models.messages import OutputMessage
from scint.framework.models.events import MethodCall


__all__ = "dictorial", "keyfob"


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
                    return obj.model_model().get(attr)
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
                return data.model_model().get(attr)
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


async def unpack_response(object, paths):
    for path in paths:
        print(object)
        name = path.split(".")[-1]
        if dictorial(object, path):
            if name == "tool_calls":
                for call in dictorial(object, path):
                    return make_arguments(call)
            elif name == "content":
                return make_message(dictorial(object, path))
            elif name == "url":
                return make_link(dictorial(object, path))
            elif name == "file":
                return make_file(dictorial(object, path))
            elif name == "embedding":
                return make_embedding(dictorial(object, path))


def make_arguments(data):
    return MethodCall(
        name=dictorial(data, "function.name"),
        arguments=json.loads(dictorial(data, "function.arguments")),
    )


def make_message(data):
    print(data)
    return OutputMessage(**json.loads(data))


def make_file(data):
    if keyfob(data, "file"):
        return {"name": "files", "path": "scint", "store": keyfob(data, "file")}
    if keyfob(data, "embedding"):
        return {"path": "scint", "store": keyfob(data, "embedding")}


def make_link(data):
    if keyfob(data, "file"):
        return {"name": "files", "path": "scint", "store": keyfob(data, "file")}
    if keyfob(data, "embedding"):
        return {"path": "scint", "store": keyfob(data, "embedding")}


def make_embedding(data):
    if keyfob(data, "file"):
        return {"name": "files", "path": "scint", "store": keyfob(data, "file")}
    if keyfob(data, "embedding"):
        return {"path": "scint", "store": keyfob(data, "embedding")}
