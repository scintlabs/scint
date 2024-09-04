import json

from scint.core.primitives.messages import OutputMessage

from .dicts import dictorial, keyfob


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
    args = dictorial(data, "function").get("arguments")
    return [str(json.loads(args))]


def make_message(data):
    print("Making message.")
    data = json.loads(data)
    message = OutputMessage(**data)
    return message


def make_file(data):
    print("Making file.")
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "store": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "store": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None


def make_link(data):
    print("Making link.")
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "store": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "store": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None


def make_embedding(data):
    print("Making embedding.")
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "store": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "store": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None
