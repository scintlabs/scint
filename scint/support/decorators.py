import functools

from scint.modules.intelligence import intelligence_controller
from scint.modules.logging import log
from scint.data.schema import Completion
from scint.data.schema import Message, AssistantMessage, Prompt, UserMessage
from scint.data.schema import Arguments


def completion(prompt: str, prompts: list = None):
    def decorator(func):
        description = "An ad-hoc completion to use for any Python function that returns a string value or a Scint message type."
        instructions = [Prompt(content="")]
        messages = []
        system_prompt = Prompt(content=prompt)
        messages.append(system_prompt)
        if prompts:
            for index, each_prompt in enumerate(prompts):
                if index % 2 == 0:
                    messages.append(AssistantMessage(content=each_prompt))
                else:
                    messages.append(UserMessage(content=each_prompt))

        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            function_instance = func(*args, **kwargs)
            async for response in function_instance:
                if isinstance(response, Message):
                    response = response.content
                elif isinstance(response, str):
                    response = response

                msg = Prompt(content=f"Summarize content: {response}")
                messages.append(msg)
                context = Completion(
                    **{
                        "name": func.__name__,
                        "description": description,
                        "instructions": instructions,
                        "messages": messages,
                    }
                )

                completion_call = intelligence_controller.parse(context)
                async for res in completion_call:
                    log.info(res)
                    yield res

        return decorated

    return decorator


def function(*args, **kwargs):
    def decorator(func):
        from scint.data.lib import functions
        from scint.modules.intelligence import intelligence_controller
        from scint.core.controller import context_controller

        # func_source = parse_function(func)
        # prompt = SystemMessage(content=f"{func_source}")
        context_controller.create_context()

        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            async for call in intelligence_controller.parse():
                if isinstance(call, Arguments):
                    pass

            func_instance = func(*args, **kwargs)
            async for response in func_instance:
                if isinstance(response, Message):
                    yield response

        return decorated

    return decorator
