from uuid import uuid4

from scint.support.types import AssistantMessage, Arguments, Message, SystemMessage
from scint.support.types import ContextData
from scint.support.logging import log
from scint.controllers.intelligence import intelligence_controller
from scint.objects.containers import ContainerType, Functions, Messages, Prompts
from scint.objects import functions


class ContextType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        id = str(uuid4())
        name = name
        parent = None
        nodes = []
        prompts = Prompts(cls)
        messages = Messages(cls)
        functions = Functions(cls)
        function_choice = dct.get("function_choice", "auto")

        def get_metadata(self, dct):
            metadata = {
                "id": id,
                "name": name,
                "parent": parent,
                "nodes": nodes,
                "prompts": [prompt.metadata for prompt in prompts],
                "messages": [message.metadata for message in messages],
                "functions": [functions.metadata for functions in functions],
                "function_choice": function_choice,
            }

            for key, value in dct.items():
                if hasattr(value, "metadata"):
                    metadata[key] = value.metadata
                if isinstance(value, ContainerType) and hasattr(value, "metadata"):
                    metadata[key] = value.metadata
                if isinstance(value, list):
                    metadata[key] = [item.metadata for item in value]
                metadata[key] = value

            self.metadata = metadata
            return self.metadata

        async def process(self, message: Message):
            log.info(f"Processing message with {self.name}")
            self.messages.append(message)
            async for res in self.intelligence.process(ContextData(**self.metadata)):
                if isinstance(res, Arguments):
                    async for new_res in self.execute(res):
                        yield new_res
                    continue

                elif isinstance(res, AssistantMessage):
                    self.messages.append(res)
                    yield res

                elif isinstance(res, SystemMessage):
                    self.messages.append(res)
                    async for system_res in self.process(res):
                        yield system_res

        async def execute(self, arguments: Arguments):
            func = getattr(functions, arguments.name)
            args = SystemMessage(content=f"{arguments.name}({arguments.content})")
            async for res in func(**arguments.content):
                self.messages.append(args)
                async for final_res in self.process(res):
                    yield final_res

        dct["id"] = id
        dct["name"] = name
        dct["parent"] = parent
        dct["nodes"] = nodes
        dct["prompts"] = prompts
        dct["messages"] = messages
        dct["functions"] = functions
        dct["function_choice"] = function_choice
        dct["process"] = process
        dct["execute"] = execute
        dct["intelligence"] = intelligence_controller
        dct["metadata"] = get_metadata(cls, dct)
        return super().__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class App(metaclass=ContextType):
    def __init__(self):
        super().__init__()
