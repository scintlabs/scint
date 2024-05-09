import ast
import functools
import inspect
import re

from scint.support.types import Context, Function, FunctionParams, List, Message
from scint.support.types import SystemMessage, AssistantMessage, UserMessage
from scint.controllers.intelligence import IntelligenceController
from scint.system.logging import log


def extract_attribute(source, attribute_name):
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


def extract_function_metadata(function):
    source = inspect.getsource(function)
    description = extract_attribute(source, "description")
    props = extract_attribute(source, "props")
    return description, props


class CallableType(type):
    name = None
    function = None
    intelligence = IntelligenceController()

    @classmethod
    def __prepare__(dct, *args, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, *args, **kwargs):
        name = dct.get("name")
        function = dct.get("function")
        source = inspect.getsource(function)
        description = extract_attribute(source, "description")
        props = extract_attribute(source, "props")
        signature = inspect.signature(function)
        required = [
            param_name
            for param_name, param in signature.parameters.items()
            if param.default == inspect.Parameter.empty and param_name != "self"
        ]

        def embedding(function):
            @functools.wraps(function)
            async def decorated(*args, **kwargs):
                function_instance = function(*args, **kwargs)
                async for result in function_instance(*args, **kwargs):
                    async for result in getattr(result.name)(**result.arguments):
                        yield result

                yield decorated

        def decorator(function):
            @functools.wraps(function)
            async def decorated(*args, **kwargs):
                function_instance = function(*args, **kwargs)
                async for result in function_instance(*args, **kwargs):
                    async for result in getattr(result.name)(**result.arguments):
                        yield result

                yield decorated

        def get_metadata(self):
            return Function(
                type="function",
                name=self.name,
                description=self.description,
                parameters=FunctionParams(
                    type="object",
                    properties=self.props,
                    required=self.required,
                ),
            )

        dct["name"] = name
        dct["description"] = description
        dct["props"] = props
        dct["required"] = required
        dct["embedding"] = embedding
        dct["decorator"] = decorator
        dct["get_metadata"] = get_metadata
        dct["intelligence"] = cls.intelligence

        return super().__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name, bases, dct, **kwargs):
        return super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


def function_factory(old_function):

    class Function(metaclass=CallableType):
        name = old_function.__name__
        function = old_function

        def call(function):
            @functools.wraps(function)
            async def decorated(*args, **kwargs):
                function_instance = function(*args, **kwargs)
                async for result in function_instance(*args, **kwargs):
                    yield result

                yield decorated

    new_function = Function()
    return new_function


def completion(prompt: str, prompts: List[str] = None):
    def decorator(function):
        description = (
            "An ad-hoc completion to use for any function that returns string values."
        )
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
            log.info(f"Calling {function.__name__}.")
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

                log.info(f"Calling completion for {function.__name__}.")
                completion_call = IntelligenceController().parse(context)
                async for res in completion_call:
                    log.info(res)
                    yield res

        return decorated

    return decorator


# def completion(function, prompt: str, prompts: List[str] = None):
#     @functools.wraps(function, prompt, prompts)
#     async def decorated(*args, **kwargs):
#         messages = [SystemMessage(content=prompt)]
#         if prompts:
#             for prompt, index in enumerate(prompts):
#                 if index % 2 == 0:
#                     messages.append(AssistantMessage(content=prompt[index]))
#                 messages.append(UserMessage(content=prompts[index]))

#         log.info(f"Calling {function.__name__}.")
#         function_instance = function(*args, **kwargs)
#         async for result in function_instance(*args, **kwargs):
#             messages.append(result)
#             log.info(f"Got {result} from {function.__name__}.")

#             intelligence = IntelligenceController()
#             context = Context(
#                 **{
#                     "name": function.__,
#                     "messages": messages,
#                     "functions": [
#                         Function(
#                             type="function",
#                             name=function.__name__,
#                             description="An ad-hoc completion to use for any function that returns string values.",
#                             parameters=FunctionParams(
#                                 type="object",
#                                 properties={
#                                     "response": {
#                                         "type": "string",
#                                         "description": "The response to the given request.",
#                                     },
#                                     "required": ["response"],
#                                 },
#                             ),
#                         )
#                     ],
#                     "function_choice": {
#                         "type": "function",
#                         "function": {"name": function.__name__},
#                     },
#                 }
#             )

#             log.info(f"Calling completion for {function.__name__}.")
#             for res in intelligence.parse(context):
#                 yield res

#         yield decorated(function)
