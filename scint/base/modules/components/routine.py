from scint.base.modules.components.component import ComponentType
from scint.support.types import (
    FunctionArguments,
    Context,
    Message,
)
from scint.support.logging import log


class Routine(metaclass=ComponentType):
    """
    This module defines a set of schemes to interact with.

    You are Scint, a highly-composable and dynamic system powered by artificial intelligence. You have access to the tools and knowledge to expand your capabilities, but pay close attention to guidelines as they shift depending on your currently active scheme and context.
    """

    async def parse(self, message: Message):
        self.messages.append(message)
        metadata = self.metadata
        log.info(metadata)
        async for response in self.intelligence.parse(Context(**metadata)):
            if isinstance(response, FunctionArguments):
                log.info(f"Calling function.")
                async for function_results in self.call_function(response, message):
                    yield function_results

            if isinstance(response, Message):
                log.info(f"Sending response to the interface.")
                async for message_response in self.interface.parse(response):
                    yield message_response
