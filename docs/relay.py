# from scint.base.components.component import ComponentType
# from scint.support.types import Arguments, Context, Message
# from scint.support.logging import log


# class Relay(metaclass=ComponentType):
#     """
#     This module defines a set of schemes to interact with.

#     You are Scint, a highly-composable and dynamic system powered by artificial intelligence. You have access to the tools and knowledge to expand your capabilities, but pay close attention to guidelines as they shift depending on your currently active scheme and context.
#     """

#     async def parse(self, message: Message):
#         self.messages.append(message)
#         metadata = self.metadata
#         log.info(metadata)
#         async for response in self.intelligence.parse(Context(**metadata)):
#             if isinstance(response, Arguments):
#                 log.info(f"Calling function.")
#                 args = response.content
#                 func_name = response.name
#                 function = getattr(self, func_name)
#                 async for function_results in function.call(message, **args):
#                     yield function_results

#             if isinstance(response, Message):
#                 yield response
