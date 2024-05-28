import time
from uuid import uuid4

from scint.modules.logging import log
from scint.modules.intelligence import intelligence_controller
from scint.core.containers import Prompts, Functions
from scint.core.models import Completion, Message, SystemMessage, Arguments
from scint.core.lib import functions


class ContextType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        async def process(self):
            log.info(f"Processing message with {self.name}")
            async for res in self.intelligence.process(Completion(**self.metadata)):
                if isinstance(res, Arguments):
                    async for new_res in self.execute(res):
                        yield new_res
                elif isinstance(res, SystemMessage):
                    self.messages.append(res)
                    async for system_res in self.process(res):
                        yield system_res
                elif isinstance(res, Message):
                    self.messages.append(res)
                    yield res
                continue
            if self.description is None and len(self.messages) > 6:
                async for res in self.define():
                    yield res

        async def execute(self, arguments: Arguments):
            log.info(f"Executing function with {self.name}")
            func = getattr(functions, arguments.name)
            async for call in func(**arguments.arguments):
                self.messages.append(call)
                async for final_res in self.process():
                    yield final_res

        def metadata(self):
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "prompts": self.prompts.metadata,
                "messages": self.messages.metadata,
                "functions": self.functions.metadata,
                "function_choice": self.function_choice,
            }

        dct["id"] = str(uuid4())
        dct["name"] = None
        dct["description"] = None
        dct["messages"] = None
        dct["prompts"] = Prompts(cls)
        dct["functions"] = Functions(cls)
        dct["function_choice"] = "auto"
        dct["process"] = process
        dct["execute"] = execute
        dct["metadata"] = property(metadata)
        dct["intelligence"] = intelligence_controller
        return super().__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class Context(metaclass=ContextType):
    def __init__(self, name, description, messages):
        super().__init__()
        self.lifetime = time.time() + 3600
        self.name = name
        self.description = description
        self.messages = messages
        self.prompts = Prompts(self)
        self.functions = Functions(self)
        self.function_choice = "auto"

    def refresh(self, prompts, functions):
        try:
            self.prompts.refresh(prompts)
            self.functions.refresh(functions)
        except Exception as e:
            log.info(f"Error refreshing context: {e}")
