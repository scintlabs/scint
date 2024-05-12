import functools
import inspect

from scint.base.modules.components.function import FuncType
from scint.support.types import Context, Function, FunctionParams, Message, Arguments
from scint.support.types import SystemMessage, AssistantMessage, UserMessage
from scint.controllers.intelligence import IntelligenceController
from scint.support.logging import log


def completion(prompt: str, prompts: list = None):
    def decorator(function):
        description = "An ad-hoc completion to use for any Python function that returns a string value or a Scint message type."
        instructions = [SystemMessage(content="")]
        messages = []
        system_prompt = SystemMessage(content=prompt)
        messages.append(system_prompt)
        if prompts:
            for index, each_prompt in enumerate(prompts):
                if index % 2 == 0:
                    messages.append(AssistantMessage(content=each_prompt))
                else:
                    messages.append(UserMessage(content=each_prompt))

        @functools.wraps(function)
        async def decorated(*args, **kwargs):
            function_instance = function(*args, **kwargs)
            async for response in function_instance:
                if isinstance(response, Message):
                    response = response.content
                elif isinstance(response, str):
                    response = response

                msg = SystemMessage(content=f"Summarize content: {response}")
                messages.append(msg)
                context = Context(
                    **{
                        "name": function.__name__,
                        "description": description,
                        "instructions": instructions,
                        "messages": messages,
                    }
                )

                completion_call = IntelligenceController().parse(context)
                async for res in completion_call:
                    log.info(res)
                    yield res

        return decorated

    return decorator


def function_call(description: str, props: dict, prompt: str, prompts: list = None):
    """An ad-hoc function call to use with vanilla Python functions. Map prop arguments to the wrapped function's arguments."""

    def decorator(function):
        signature = inspect.signature(function)
        required = [
            param_name
            for param_name, param in signature.parameters.items()
            if param.default == inspect.Parameter.empty and param_name != "self"
        ]

        function_metadata = Function(
            type="function",
            name=function.__name__,
            description=description,
            parameters=FunctionParams(
                type="object", properties=props, required=required
            ),
        )

        messages = []
        messages.append(SystemMessage(content=prompt))
        if prompts:
            for index, each_prompt in enumerate(prompts):
                if index % 2 == 0:
                    messages.append(AssistantMessage(content=each_prompt))
                else:
                    messages.append(UserMessage(content=each_prompt))

        context = Context(
            **{
                "name": function.__name__,
                "description": description,
                "instructions": [],
                "messages": messages,
                "functions": [function_metadata],
                "function_choice": {
                    "type": "function",
                    "function": {"name": function.__name__},
                },
            }
        )

        @functools.wraps(function)
        async def decorated(*args, **kwargs):
            function_call = IntelligenceController().parse(context)
            async for call in function_call:
                if isinstance(call, Arguments):
                    kwargs = call.arguments

            function_instance = function(*args, **kwargs)
            async for response in function_instance:
                if isinstance(response, Message):
                    yield response

        return decorated

    return decorator


def embedding(function):
    @functools.wraps(function)
    async def decorated(*args, **kwargs):
        function_instance = function(*args, **kwargs)
        async for result in function_instance(*args, **kwargs):
            async for result in getattr(result.name)(**result.arguments):
                yield result

        yield decorated


def metadata(description: str, props: dict, *args, **kwargs):
    def decorator(argument):
        d = description
        p = props

        class Func(metaclass=FuncType):
            description = d
            props = p
            function = argument

            @functools.wraps(argument)
            async def call(*args, **kwargs):
                async for result in argument(*args, **kwargs):
                    yield result

        func = Func()
        return func

    return decorator
