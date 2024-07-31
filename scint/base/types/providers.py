from scint.base.models import generate_id
from scint import settings


__all__ = (
    "IntelligenceProvider",
    "ConnectionProvider",
    "SearchProvider",
    "StorageProvider",
    "QueueProvider",
)


class ProviderType(type):
    @classmethod
    def __prepare__(cls, name, bases, *args, **kwargs):
        return {**settings.app.as_dict()}

    def __new__(cls, name, bases, dct, *args, **kwargs):
        cls.address = generate_id(name)
        cls.studio = None
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, *args, **kwargs):
        super().__init__(name, bases, dct, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class IntelligenceProvider(metaclass=ProviderType):
    def __init__(self):
        super().__init__()


class MessageProvider(metaclass=ProviderType):
    def __init__(self):
        super().__init__()


class SearchProvider(metaclass=ProviderType):
    def __init__(self):
        super().__init__()


class StorageProvider(metaclass=ProviderType):
    def __init__(self):
        super().__init__()


class QueueProvider(metaclass=ProviderType):
    def __init__(self):
        super().__init__()
