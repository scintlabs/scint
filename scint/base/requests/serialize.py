import json
from typing import Dict

from pydantic import BaseModel


from ..components.prompts.prompts import Message
from ..utils import keyfob, dictorial


class Model(BaseModel):
    pass


class FunctionCall(Model):
    name: str
    type: str
    arguments: Dict[str, object]


async def unpack_response(object, paths):
    print("Unpacking response.")
    for path in paths:
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
    print("Making arguments.")
    name = dictorial(data, "function.name")
    args = dictorial(data, "function").get("arguments")
    return FunctionCall(name=name, arguments=str(json.loads(args)))


def make_message(data):
    print("Making message.")
    message = Message(body=json.loads(data))
    print(message)
    return message


def make_file(data):
    print("Making file.")
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "data": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "data": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None


def make_link(data):
    print("Making link.")
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "data": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "data": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None


def make_embedding(data):
    print("Making embedding.")
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "data": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "data": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None
