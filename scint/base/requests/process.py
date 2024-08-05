from ..requests.schema import Request
from ..requests.serialize import unpack_response
from ..utils import dictorial
from scint.base.settings import Settings

from openai import AsyncOpenAI

settings = Settings()
config = settings.services.intelligence.settings.as_dict()
template = lambda r, c: {"role": r, "data": c}  # type: ignore
methods = ["scint.ensemble", "image", "speech", "embedding"]
get_preset = lambda p: dictorial(config, f"presets.{p}")
get_provider = lambda p: dictorial(config, f"support.{p}")
attrlist = lambda l, t: all(hasattr(i, t) for i in l)

# TODO: Refactor and move most of these to the actual models being built and serialized


async def process_request(request: Request):
    print("Processing request.")
    try:
        req, method, paths = await parse_request(request)
        result = await method(**req)
        return await unpack_response(result, paths)
    except Exception as e:
        print(f"Error processing intelligence request: {e}")


async def parse_request(request: Request):
    print("Parsing request.")
    presets = config.get("presets")
    providers = config.get("providers")
    try:
        preset = presets.get(request.parameters.preset)
        provider = providers.get(request.parameters.provider)
        params = provider.get("format").get(request.parameters.format)
        new_request = await create_request(request, preset)
        method = params.get("method")
        func = eval(method)
        return new_request, func, provider.get("response_paths")
    except Exception as e:
        print(f"Error parsing intelligence request: {e}")
        return None, None, None


async def create_request(request, preset):
    print("Creating request.")
    try:
        req = {**preset}
        req["messages"] = [message.build() for message in request.messages]
        if request.functions:
            req["tools"] = [function.build() for function in request.functions]
            req["tool_choice"] = "auto"
        return req
    except Exception as e:
        print(f"Error creating intelligence request: {e}")
        return None


async def invoke(command):
    async def _invoke(request):
        paths = dictorial(get_provider("openai"), "response_paths")
        response = await unpack_response(request, paths)
        return response

    callable = dictorial(get_provider("openai"), f"format.completion.method")
    params = create_request(command)
    invocation = await callable(**params)
    arguments = await _invoke(invocation)
    return arguments


async def request_embedding(config, input: str):
    try:
        provider = dictorial(config, "support.openai")
        method = dictorial(provider, "format.embedding.method")
        result = await method(model="text-embedding-3-small", input=input)
        embedding = dictorial(result, "data.0.embedding")
        return {"data": embedding}
    except Exception as e:
        print(f"Error embedding message: {e}")


async def request_completion(prompt: str):
    try:
        provider = dictorial("support.openai")
        method = dictorial(provider, "format.completion.method")
        async for result in method(prompt, model="gpt4"):
            embedding = dictorial(result, "message.0.content")
            return {"data": embedding}
    except Exception as e:
        print(f"Error embedding message: {e}")
