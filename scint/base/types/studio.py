from scint.base.models.messages import Message
from scint.base.models import generate_id

__all__ = "StudioType", "Studio", "Space"


class StudioType(type):
    _instance = None

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        dct["_id"] = generate_id(name)
        dct["_instance"] = cls
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, *args, **kwargs):
        super().__init__(name, bases, dct, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class Studio(metaclass=StudioType):
    def __init__(self):
        super().__init__()

    async def send_message(message: Message):
        print(message)

    async def broadcast_message(message: Message):
        print(message)


class Space(metaclass=StudioType):
    def __init__(self):
        super().__init__()

    async def send_message(message: Message):
        print(message)

    async def broadcast_message(message: Message):
        print(message)
