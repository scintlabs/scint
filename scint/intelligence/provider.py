import json
from uuid import uuid4


from scint.settings.intelligence import intelligence_config
from scint.intelligence.models import Model, ModelProvider, Request
from scint.messaging.models import Arguments, AssistantMessage, Function, Message
from scint.support.utils import dictorial, keyfob
from scint.support.logging import log
from scint.support.types import Dict, List, Optional


class IntelligenceProvider:
    def __init__(self):
        self._providers = intelligence_config.get("providers")
        self._presets = intelligence_config.get("presets")

    async def process(self, request: Request):
        log.info(f"Processing request.")
        try:
            req, method, paths = await self._parse_request(request)
            result = await method(**req)
            response = await unpack_response(result, paths)
            yield response
        except Exception as e:
            log.error(f"Error processing intelligence request: {e}")

    async def _parse_request(self, request: Request):
        log.info(f"Parsing request.")
        try:
            preset = self._presets.get(request.parameters.preset)
            provider = self._get_provider(request.parameters.provider)
            params = provider.get("format").get(request.parameters.format)
            new_request = await self._create_request(request, preset)
            return new_request, params.get("method"), provider.get("response_paths")
        except Exception as e:
            log.error(f"Error parsing intelligence request: {e}")
            return None, None, None

    async def _create_request(self, context, preset):
        log.info(f"Creating intelligence request from context.")
        try:
            request = {**preset, "messages": [], "tools": []}
            for prompt in context.prompts:
                request["messages"].append(prompt.metadata)
            for message in context.messages:
                request["messages"].append(message.metadata)
            for function in context.functions:
                request["tools"].append(function.metadata)
            if context.function_choice and context.function_choice is not None:
                request["function_choice"] = context.function_choice
            return request
        except Exception as e:
            log.error(f"Error creating intelligence request: {e}")
            return None

    def _load_providers(self, cfgs: Dict[str, Dict]):
        log.info(f"Loading intelligence providers.")
        providers = {}
        for provider_name, provider_config in cfgs.items():
            models = [Model(**cfg) for cfg in provider_config["models"]]
            providers[provider_name] = ModelProvider(name=provider_name, models=models)
        return providers

    def _get_provider(self, provider: str, key: Optional[str] = None):
        log.info(f"Getting intelligence provider.")
        provider = self._providers.get(provider)
        if key and provider:
            return next((model for model in provider.models if model.name == key), None)
        return provider


intelligence = IntelligenceProvider()


methods = ["completion", "image", "speech", "embedding"]
get_preset = lambda p: dictorial(intelligence_config, f"presets.{p}")  # type: ignore
get_provider = lambda p: dictorial(intelligence_config, f"providers.{p}")  # type: ignore


async def invoke(command):
    async def _call(request):
        paths = dictorial(get_provider("openai"), "response_paths")
        response = await unpack_response(request, paths)
        return response

    callable = dictorial(get_provider("openai"), f"format.completion.method")
    params = build_request(command)
    invocation = await callable(**params)
    arguments = await _call(invocation)
    return arguments


def build_request(command):
    request = {**get_preset("balanced")}
    instructions = dictorial(command, "instructions")
    context = dictorial(command, "context")
    functions = dictorial(command, "functions")
    request["messages"] = build_messages(instructions, context)
    request["tools"], request["tool_choice"] = build_function(function, True)
    return request


def build_messages(instructions, context):
    template = lambda r, c: {"role": r, "content": c}  # type: ignore
    messages = []
    for instruction in instructions:
        messages.append(template("system", instruction.get("content")))
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


async def request_embedding(input: str):
    try:
        provider = dictorial(intelligence_config, "providers.openai")
        method = dictorial(provider, "format.embedding.method")
        result = await method(model="text-embedding-3-small", input=input)
        embedding = dictorial(result, "data.0.embedding")
        return {"data": embedding}
    except Exception as e:
        log.error(f"Error embedding message: {e}")


async def request_completion(prompt: str):
    try:
        provider = dictorial(intelligence_config, "providers.openai")
        method = dictorial(provider, "format.completion.method")
        async for result in method(prompt, model="gpt4"):
            embedding = dictorial(result, "message.0.content")
            return {"data": embedding}
    except Exception as e:
        log.error(f"Error embedding message: {e}")


def make_message(data):
    return AssistantMessage(
        content=keyfob(data, "content"),
        annotations=keyfob(data, "annotations"),
        embedding=keyfob(data, "embedding"),
    )


def make_arguments(data):
    name = dictorial(data, "function.name")
    args = dictorial(data, "function").get("arguments")
    return Arguments(name=name, arguments=json.loads(args))


def make_artifact(data):
    try:
        if keyfob(data, "file"):
            return {"name": "files", "path": "scint", "data": keyfob(data, "file")}
        if keyfob(data, "embedding"):
            return {"path": "scint", "data": keyfob(data, "embedding")}
    except (KeyError, IndexError, AttributeError):
        return None


async def unpack_response(object, paths):
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
