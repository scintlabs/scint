import datetime
from uuid import uuid4

import numpy as np

from scint.core.data.containers.blocks import Block
from scint.core.data.metadata import gather_metadata
from scint.messaging.models import Message, SystemMessage
from scint.support.logging import log


class Collection:
    def __init__(self):
        self.id = str(uuid4())
        self.name = "New Collection"
        self.description = "New Collection"
        self.data = []
        self.embedding = np.array([])
        self.datatype = self._datatype
        self.metadata = self._metadata

    @property
    def _datatype(self):
        if self.data:
            if type(self.data[0]) is not None:
                return type(self.data[0])
        return type(any)

    @property
    def _metadata(self):
        md = {}
        for key, value in self.__dict__.items():
            if key in ["id", "messages"]:
                md[key] = value
            if key == "data":
                md[key] = [item.metadata for item in value]
        return md

    def add(self, obj):
        if isinstance(obj, self.datatype):
            if obj in self.data:
                self.core.append(obj)

    def replace(self, list):
        old = self.core.copy()
        self.data = list

    def remove(self, obj):
        if obj in self.data:
            removed = self.core.pop(obj)
            del removed

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


class Prompts(Collection):
    def __init__(self):
        super().__init__()

    def extend(self, prompts):
        return self.core.extend(prompts)

    def insert(self, prompt, category):
        if category == "status":
            self.core.insert(
                0,
                SystemMessage(
                    content=[
                        Block(
                            data=f"The current time is {datetime.now()} You're currently connect to Discord. Pay attention to usernames."
                        )
                    ]
                ),
            )
            log.info(f"Set {category} prompt.")
        if category == "identities" and prompt is not None:
            self.core.insert(1, prompt)
            log.info(f"Set {category} prompt.")
        elif category == "instructions" and prompt is not None:
            self.core.insert(2, prompt)
            log.info(f"Set {category} prompt.")
        elif category == "modifier" and prompt is not None:
            self.core.insert(3, prompt)
            log.info(f"Set {category} prompt.")
        elif category == "people" and prompt is not None:
            self.core.insert(4, prompt)
            log.info(f"Set {category} prompt.")
        else:
            log.info("Invalid prompt category.")
        return


class Messages(Collection):
    def __init__(self):
        super().__init__()

    def append(self, message: Message):
        self.core.append(message)

    def insert(self, index, message: Message):
        self.core.insert(index, message)


class Functions(Collection):
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


class Files(Collection):
    def __init__(self):
        super().__init__()
