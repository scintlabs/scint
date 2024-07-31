from scint.base.models.messages import Message
from scint.base.utils import generate_id
from scint import settings


__all__ = "Library", "Archive"


class LibraryType(type):
    _instance = None

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # providers = {}
        # for key, value in settings.app.as_dict().items():
        #     provider = get_module(key, value)
        #     print(provider)
        #     if provider:
        #         providers[key] = provider

        # return {"_providers": providers}
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


class Library(metaclass=LibraryType, settings=settings):
    def __init__(self, settings=settings):
        super().__init__()

    async def send_message(message: Message):
        print(message)

    async def broadcast_message(message: Message):
        print(message)


class Archive(metaclass=LibraryType, settings=settings):
    def __init__(self, settings=settings):
        super().__init__()

    async def send_message(message: Message):
        print(message)

    async def broadcast_message(message: Message):
        print(message)
