import asyncio
import types

from scint.support.types import (
    Arguments,
    Context,
    Message,
    SystemMessage,
)
from scint.support.logging import log


# class ScopeType(type):
#     description = None
#     instructions = []
#     intelligence = IntelligenceController

#     @classmethod
#     def __prepare__(dct, *args, **kwargs):
#         return {}

#     def __new__(cls, name, bases, dct, **kwargs):
#         name = name
#         functions = []
#         docstring = dct.get("__doc__", "")
#         description, *instructions = docstring.strip().split("\n\n")
#         instructions = [SystemMessage(content=item.strip()) for item in instructions]

#         for attr_name, attr_value in dct.items():
#             if isinstance(attr_value, types.FunctionType):
#                 functions.append(function_factory(attr_value))

#         async def parse(self, message: Message):
#             log.info(f"{self.name} is parsing a message: {message}")
#             self.messages.append(message)
#             metadata = self.get_metadata()
#             async for response in self.intelligence.parse(Context(**metadata)):
#                 if isinstance(response, Arguments):
#                     async for response in self.call(response.name, response):
#                         yield response

#                 elif isinstance(response, SystemMessage):
#                     yield response

#         async def call(self, function_name: str, message: Message):
#             log.info(f"Calling function: {function_name}")
#             function = getattr(self, function_name, None)
#             async for response in function(**message.content):
#                 yield response

#         async def compose_message(self, receiver: str, topic: str, content: str):
#             description = "Use this function to create response messages."
#             props = {
#                 "receiver": {
#                     "type": "string",
#                     "description": "The receiver of the message.",
#                 },
#                 "topic": {
#                     "type": "string",
#                     "description": "The topic of the message, usually a reference to a recently completed task.",
#                 },
#                 "content": {
#                     "type": "string",
#                     "description": "The content of the message. If the message is a response or update regarding a task, this should be a short summary of the results.",
#                 },
#             }

#             yield AssistantMessage(receiver=receiver, topic=topic, content=content)

#         def get_metadata(self):
#             return {
#                 "name": self.name,
#                 "description": self.description,
#                 "instructions": [item.get_metadata() for item in self.instructions],
#                 "messages": [message.get_metadata() for message in self.messages],
#                 "functions": [func.get_metadata() for func in self.functions],
#             }

#         dct["name"] = name
#         dct["description"] = description
#         dct["instructions"] = instructions
#         dct["messages"] = Container(name)
#         dct["functions"] = functions
#         dct["parse"] = parse
#         dct["compose_message"] = compose_message
#         dct["call"] = call
#         dct["get_metadata"] = get_metadata
#         dct["intelligence"] = IntelligenceController()
#         return super().__new__(cls, name, bases, dct, **kwargs)

#     def __init__(cls, name, bases, dct):
#         dct["messages"] = cls.messages
#         dct["functions"] = cls.functions

#         return type.__init__(cls, name, bases, dct)

#     def __call__(cls, *args, **kwargs):
#         instance = super().__call__(*args, **kwargs)
#         instance.messages = cls.messages
#         instance.functions = cls.functions
#         return instance


# class Scope(metaclass=ScopeType):
#     """
#     This is a default scope.

#     This is a default scope.
#     """


class ScopeType(type):
    def __new__(cls, name, bases, dct, **kwargs):
        functions = []
        docstring = dct.get("__doc__", "")
        description, *instructions = docstring.strip().split("\n\n")
        instructions = [SystemMessage(content=item.strip()) for item in instructions]

        async def parse(self, message: Message):
            log.info(f"{self.name} is parsing a message: {message}")
            self.messages.append(message)
            metadata = self.get_metadata()
            async for response in self.intelligence.parse(Context(**metadata)):
                if isinstance(response, Arguments):
                    async for response in self.call(response.name, response):
                        yield response

                elif isinstance(response, SystemMessage):
                    yield response

        async def call(self, function_name: str, message: Message):
            log.info(f"Calling function: {function_name}")
            function = getattr(self, function_name, None)
            async for response in function(**message.content):
                yield response

        dct["name"] = name
        dct["description"] = description
        dct["instructions"] = instructions
        dct["parse"] = parse
        dct["call"] = call
        return super().__new__(cls, name, bases, dct, **kwargs)


class Scope(ScopeType):
    """
    This is a default scope.

    This is a default scope.
    """
