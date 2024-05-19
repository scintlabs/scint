from datetime import datetime
from uuid import uuid4
from scint.controllers.storage import storage_controller
from scint.support.types import Message, SystemMessage
from scint.support.logging import log


class ContainerType(type):
    def __new__(cls, name, bases, dct, **kwargs):
        id = str(uuid4())
        name = name
        context = kwargs.get("context")
        data = []

        def get_metadata(self, dct):
            self.metadata = {
                "id": id,
                "name": name,
                "context": context,
                "data": data,
            }
            for key, value in dct.items():
                if hasattr(value, "metadata"):
                    self.metadata[key] = value.metadata
                if isinstance(value, ContainerType) and hasattr(value, "metadata"):
                    self.metadata[key] = value.metadata
                if isinstance(value, list) and hasattr(all(value), "metadata"):
                    self.metadata[key] = [item.metadata for item in value]
                self.metadata[key] = value

            return self.metadata

        dct["id"] = id
        dct["name"] = name
        dct["context"] = context
        dct["data"] = []
        dct["__getitem__"] = cls.__getitem__
        dct["__setitem__"] = cls.__setitem__
        dct["__len__"] = cls.__len__
        dct["__iter__"] = cls.__iter__
        dct["storage"] = storage_controller
        dct["metadata"] = get_metadata(cls, dct)
        return super().__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.context = args[0]
        return instance

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


class Prompts(metaclass=ContainerType):
    def __init__(self, context):
        super().__init__()

    def set_prompt(self, prompt_type: str, prompt=None):
        if prompt_type == "status":
            status = datetime.now().isoformat()
            prompt = SystemMessage(content=f"Current date and time: {status}")
            log.info(f"Setting {prompt_type}: {prompt}")
            self.data.insert(0, prompt)

        elif prompt_type == "instructions" and prompt is not None:
            log.info(f"Setting {prompt_type} prompt.")
            self.data.insert(1, prompt)
        elif prompt_type == "identity" and prompt is not None:
            log.info(f"Setting {prompt_type} prompt.")
            self.data.insert(2, prompt)
        elif prompt_type == "modifier" and prompt is not None:
            log.info(f"Setting {prompt_type} prompt.")
            self.data.insert(3, prompt)
        elif prompt_type == "user" and prompt is not None:
            log.info(f"Setting {prompt_type} prompt.")
            self.data.insert(4, prompt)
        else:
            log.info("Invalid prompt type.")


class Messages(metaclass=ContainerType):
    def __init__(self, context):
        super().__init__()

    def append(self, message: Message):
        self.data.append(message)
        self.storage.save_message(self.context, message)
        return log.info(f"Appended message to container.")

    def insert(self, index, message: Message):
        self.data.insert(index, message)
        log.info(f"Inserted message into container.")


class Functions(metaclass=ContainerType):
    def __init__(self, context):
        super().__init__()

    def refresh(self, functions):
        log.info(f"Refreshing functions.")
        self.data = functions


class Files(metaclass=ContainerType):
    def __init__(self, context):
        super().__init__()

    def append(self, message: Message):
        log.info(f"Appending message to container.")
        self.data.append(message)
