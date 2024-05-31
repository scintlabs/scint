import datetime
from uuid import uuid4

from scint.modules.logging import log
from scint.modules.storage import storage_controller
from scint.data.schema import Message, Prompt


class ContainerType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        def metadata(self):
            return {
                "id": self.id,
                "name": self.name,
                "tags": self.tags,
                "description": self.description,
                "embedding": self.embedding,
                "data": [item.metadata for item in self.data],
            }

        dct["id"] = str(uuid4())
        dct["name"] = name
        dct["tags"] = []
        dct["description"] = None
        dct["data"] = []
        dct["embedding"] = []
        dct["metadata"] = property(metadata)
        dct["storage"] = storage_controller
        dct["__getitem__"] = cls.__getitem__
        dct["__setitem__"] = cls.__setitem__
        dct["__len__"] = cls.__len__
        dct["__iter__"] = cls.__iter__
        return super().__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


class Functions(metaclass=ContainerType):
    def __init__(self):
        super().__init__()

    def refresh(self, functions):
        try:
            log.info(f"Refreshing functions.")
            self.data = functions
        except Exception as e:
            log.info(f"Error refreshing functions: {e}")

    def clear(self):
        log.info(f"Clearing functions.")
        self.data = []
        return


class Prompts(metaclass=ContainerType):
    def __init__(self):
        super().__init__()

    def insert(self, prompt, category):

        if category == "status":
            self.data.insert(
                0,
                Prompt(
                    content=f"The current time is {datetime.now()} You're currently connect to Discord. Pay attention to usernames."
                ),
            )
            log.info(f"Set {category} prompt.")
        if category == "identity" and prompt is not None:
            self.data.insert(1, prompt)
            log.info(f"Set {category} prompt.")
        elif category == "instructions" and prompt is not None:
            self.data.insert(2, prompt)
            log.info(f"Set {category} prompt.")
        elif category == "modifier" and prompt is not None:
            self.data.insert(3, prompt)
            log.info(f"Set {category} prompt.")
        elif category == "people" and prompt is not None:
            self.data.insert(4, prompt)
            log.info(f"Set {category} prompt.")
        else:
            log.info("Invalid prompt category.")
        return


class Messages(metaclass=ContainerType):
    def __init__(self):
        super().__init__()

    def append(self, message: Message):
        self.data.append(message)

    def insert(self, index, message: Message):
        self.data.insert(index, message)


class Files(metaclass=ContainerType):
    def __init__(self):
        super().__init__()

    def append(self, message: Message):
        log.info(f"Appending message to container.")
        self.data.append(message)


class Images(metaclass=ContainerType):
    def __init__(self):
        super().__init__()

    def append(self, message: Message):
        log.info(f"Appending message to container.")
        self.data.append(message)


class Links(metaclass=ContainerType):
    def __init__(self):
        super().__init__()

    def append(self, message: Message):
        log.info(f"Appending message to container.")
        self.data.append(message)


class Events(metaclass=ContainerType):
    def __init__(self):
        super().__init__()

    def append(self, message: Message):
        log.info(f"Appending message to container.")
        self.data.append(message)
