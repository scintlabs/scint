import functools

from scint.support.types import ContextData
from scint.support.types import SystemMessage, AssistantMessage, UserMessage, Message
from scint.controllers.intelligence import intelligence_controller
from scint.support.logging import log


def completion(prompt: str, prompts: list = None):
    """
    """
    def decorator(func):
        """
        """
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


        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            """
            """
            function_instance = func(*args, **kwargs)
            async for response in function_instance:
                if isinstance(response, Message):
                    response = response.content
                elif isinstance(response, str):
                    response = response

                msg = SystemMessage(content=f"Summarize content: {response}")
                messages.append(msg)
                context = ContextData(
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
#
#
# def function(*args, **kwargs):
#     def decorator(func):
#         from scint.objects import functions
#         from scint.controllers.intelligence import intelligence_controller
#         from scint.controllers.context import context_controller
#
#         func_source = parse_function(func)
#         prompt = SystemMessage(content=f"{func_source}")
#         context_controller.create_context()
#
#
#         @functools.wraps(func)
#         async def decorated(*args, **kwargs):
#             async for call in intelligence_controller.parse():
#                 if isinstance(call, Arguments):
#                     pass
#
#             func_instance = func(*args, **kwargs)
#             async for response in func_instance:
#                 if isinstance(response, Message):
#                     yield response
# 
#         return decorated
#
#     return decorator
