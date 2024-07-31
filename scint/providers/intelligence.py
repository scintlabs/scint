from typing import Optional


from scint.base.models.requests import Request
from scint.base.types.providers import ProviderType
from scint.base.models import dictorial, build_function, build_messages, unpack_response
from scint import Settings


settings = Settings()
settings.load_json("settings/providers.json", "providers")
intelligence = settings.providers.intelligence.as_dict()

methods = ["completion", "image", "speech", "embedding"]
get_preset = lambda p: dictorial(settings, f"presets.{p}")  # type: ignore
get_provider = lambda p: dictorial(f"providers.{p}")  # type: ignore
providers = intelligence.get("providers")
presets = intelligence.get("presets")


class IntelligenceProvider(metaclass=ProviderType):
    def __init__(self):
        super().__init__()
        self._providers = providers
        self._presets = presets

    def get_preset(self, preset):
        return lambda preset: dictorial(self._presets, preset)  # type: ignore

    def get_provider(self, provider: str, key: Optional[str] = None):
        return (
            get_provider(provider)
            if not key
            else dictorial(get_provider(provider), key)
        )


async def process(request: Request):
    print(f"Processing request.")
    try:
        req, method, paths = await parse_request(request)
        result = await method(**req)
        response = await unpack_response(result, paths)
        yield response
    except Exception as e:
        print(f"Error processing intelligence request: {e}")


async def parse_request(request: Request):
    print(f"Parsing request.")
    try:
        preset = get_preset("balanced")
        provider = get_provider(request.parameters.provider)
        params = provider.get("format").get(request.parameters.format)
        return (
            await create_request(request, preset),
            params.get("method"),
            provider.get("response_paths"),
        )
    except Exception as e:
        print(f"Error parsing intelligence request: {e}")
        return None, None, None


async def create_request(self, context, preset):
    print(f"Creating intelligence request from context.")
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
        print(f"Error creating intelligence request: {e}")
        return None


async def invoke(function, *args, **kwargs):
    provider = get_provider("openai")
    caller = dictorial(provider, "format.completion.method")
    paths = dictorial(provider, "response_paths")
    params = build_request(function)
    invocation = await caller(**params)
    return await unpack_response(invocation, paths)


def build_request(function):
    preset = get_preset("balanced")
    instructions = dictorial(function, "instructions")
    context = dictorial(function, "context")
    request = {
        **preset,
        "messages": build_messages(instructions, context),
        "tools": build_function(function, True),
    }
    return request
