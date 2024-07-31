import json

from scint.base.models.messages import Message
from scint.base.models.functions import Function, FunctionCall
from scint.base.utils import keyfob, dictorial

# TODO: Refactor and move most of these to the actual models being built and serialized

template = lambda r, c: {"role": r, "data": c}  # type: ignore
methods = ["scint.ensemble", "image", "speech", "embedding"]
get_preset = lambda p: dictorial(intelligence, f"presets.{p}")  # type: ignore
get_provider = lambda p: dictorial(intelligence, f"providers.{p}")  # type: ignore
attrlist = lambda l, t: all(hasattr(i, t) for i in l)  # type: ignore
rules = lambda c: dictorial(config, f"filetype.{lang}.rules.all.{c}")  # type: ignore


async def process_request(request):
    try:
        req, method, paths = await parse_request(request)
        result = await method(**req)
        return await unpack_response(result, paths)
    except Exception as e:
        print(f"Error processing intelligence request: {e}")


async def parse_request(config, request):
    try:
        preset = config.presets.get(request.parameters.preset)
        provider = config.get_provider(request.parameters.provider)
        params = provider.get("format").get(request.parameters.format)
        new_request = await create_request(request, preset)
        return new_request, params.get("method"), provider.get("response_paths")
    except Exception as e:
        print(f"Error parsing intelligence request: {e}")
        return None, None, None


async def create_request(request, preset):
    try:
        req = {**preset}
        messages = []
        tools = []
        if request.status and request.status is not None:
            messages.append(request.status.metadata)
        if request.identity and request.identity is not None:
            messages.append(request.identity.metadata)
        if request.instructions and request.instructions is not None:
            messages.append(request.instructions.metadata)
        if request.modifier and request.instructions is not None:
            messages.append(request.modifier.metadata)
        for message in request.messages:
            messages.append(message.metadata)
        for function in request.functions:
            tools.append(function.metadata)
        req["tool_choice"] = "auto"
        req["messages"] = messages
        req["tools"] = tools
        return req
    except Exception as e:
        print(f"Error creating intelligence request: {e}")
        return None


def serialize_message(data):
    data = {"data": [{"type": "text", "data": data}]}
    message = Message(**data)
    return message


def serialize_arguments(data):
    name = dictorial(data, "function.name")
    args = dictorial(data, "function").get("arguments")
    return FunctionCall(name=name, arguments=json.loads(args))


def serialize_file(data):
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "data": keyfob(data, "file")}
    except (KeyError, IndexError, AttributeError):
        return None


def serialize_link(data):
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "data": keyfob(data, "file")}
    except (KeyError, IndexError, AttributeError):
        return None


def serialize_embedding(data):
    try:
        if keyfob(data, "embedding"):
            return {"path": "scint", "data": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None


async def serialize_response(object, paths):
    for path in paths:
        name = path.split(".")[-1]
        if dictorial(object, path):
            if name == "tool_calls":
                for call in dictorial(object, path):
                    return serialize_arguments(call)
            elif name == "content":
                return serialize_message(dictorial(object, path))
            elif name == "url":
                return serialize_link(dictorial(object, path))
            elif name == "file":
                return serialize_file(dictorial(object, path))
            elif name == "embedding":
                return serialize_embedding(dictorial(object, path))


def build_request(context):
    request = {**get_preset("balanced")}
    prompts = dictorial(context, "prompts")
    if prompts is not None:
        context.extend(prompts)
    messages = dictorial(context, "messages")
    if messages is not None:
        context.extend(messages)
    functions = dictorial(context, "functions")
    if context is not None:
        request["messages"] = build_messages(context)
    if functions is not None:
        request["tools"], request["tool_choice"] = build_function(functions, False)
    return request


def build_messages(context):
    template = lambda r, c: {"role": r, "content": c}  # type: ignore
    messages = []
    for item in context:
        messages.append(template("user", item.get("content")))
    return messages


def build_function(function, force=False):
    function = [
        {
            "type": "function",
            "function": {
                "name": keyfob(function, "name"),
                "description": keyfob(function, "description"),
                "parameters": keyfob(function, "parameters"),
            },
        }
    ]
    choice = {"type": "function", "function": {"name": keyfob(function, "name")}}
    if not force:
        return function
    return function, choice


async def invoke(command):
    async def _invoke(request):
        paths = dictorial(get_provider("openai"), "response_paths")
        response = await unpack_response(request, paths)
        return response

    callable = dictorial(get_provider("openai"), f"format.completion.method")
    params = build_request(command)
    invocation = await callable(**params)
    arguments = await _invoke(invocation)
    return arguments


async def request_embedding(config, input: str):
    try:
        provider = dictorial(config, "providers.openai")
        method = dictorial(provider, "format.embedding.method")
        result = await method(model="text-embedding-3-small", input=input)
        embedding = dictorial(result, "data.0.embedding")
        return {"data": embedding}
    except Exception as e:
        print(f"Error embedding message: {e}")


async def unpack_response(object, paths):
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
    name = dictorial(data, "function.name")
    args = dictorial(data, "function").get("arguments")
    return Function(name=name, arguments=json.loads(args))


def make_message(data):
    return Message(
        content=keyfob(data, "content"),
        annotations=keyfob(data, "annotations"),
        embedding=keyfob(data, "embedding"),
    )


def make_file(data):
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "data": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "data": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None


def make_link(data):
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "data": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "data": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None


def make_embedding(data):
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "data": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "data": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None


async def request_completion(prompt: str):
    try:
        provider = dictorial("providers.openai")
        method = dictorial(provider, "format.completion.method")
        async for result in method(prompt, model="gpt4"):
            embedding = dictorial(result, "message.0.content")
            return {"data": embedding}
    except Exception as e:
        print(f"Error embedding message: {e}")


async def request_embedding(config, input: str):
    print("Requesting embedding.")
    try:
        provider = dictorial(config, "providers.openai")
        method = dictorial(provider, "format.embedding.method")
        result = await method(model="text-embedding-3-small", input=input)
        return dictorial(result, "data.0.embedding")
    except Exception as e:
        print(f"Error embedding message: {e}")
