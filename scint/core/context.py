import time
from uuid import uuid4

from scint.modules.logging import log
from scint.modules.intelligence import intelligence_controller
from scint.core.containers import Prompts, Functions
from scint.data.schema import Completion, Message, Arguments
from scint.data.lib import functions


class ContextType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        def metadata(self):
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "prompts": self.prompts.data,
                "messages": self.messages.data,
                "functions": self.functions.data,
                "function_choice": self.function_choice,
            }

        dct["id"] = str(uuid4())
        dct["name"] = None
        dct["description"] = None
        dct["prompts"] = Prompts()
        dct["functions"] = Functions()
        dct["function_choice"] = "auto"
        dct["metadata"] = property(metadata)
        dct["process"] = cls.process
        dct["execute"] = cls.execute
        dct["contextualize_struct"] = cls.contextualize_struct
        dct["intelligence"] = intelligence_controller
        return super().__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance

    def contextualize_struct(self, struct):
        self.name = struct.name
        self.description = struct.description
        self.messages = struct.messages

    async def process(self):
        log.info(f"Processing message with {self.name}")
        async for res in self.intelligence.process(Completion(**self.metadata)):
            if isinstance(res, Arguments):
                async for func_res in self.execute(res):
                    yield func_res

            elif isinstance(res, Message):
                self.messages.append(res)
                yield res

    async def execute(self, arguments: Arguments):
        log.info(f"Executing function with {self.name}")
        func = getattr(functions, arguments.name)
        async for new_res in func(**arguments.arguments):
            self.messages.append(new_res)
            async for final_res in self.process():
                yield final_res


class Context(metaclass=ContextType):
    def __init__(self):
        super().__init__()
        self.lifetime = time.time() + 3600

    def refresh(self, prompts, functions):
        try:
            self.prompts.refresh(prompts)
            self.functions.refresh(functions)
        except Exception as e:
            log.info(f"Error refreshing context: {e}")
