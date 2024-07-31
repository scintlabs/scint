from types import SimpleNamespace

from scint.base.utils.attrs import get_module
from scint.base.models import generate_id
from scint import Settings

settings = Settings()
settings.load_json("settings/providers.json", "providers")


class InterfaceType(type):
    _instance = None

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        providers = {}
        for key, value in settings.providers.as_dict().items():
            module_name = key
            module_path = value.get("import_path")
            module = get_module(module_path, module_name)
            if module:
                providers[name.lower()] = module

        return {"_providers": providers}

    def __new__(cls, name, bases, dct, **kwargs):
        cls._id = generate_id(name)
        cls._instance = cls
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, *args, **kwargs):
        cls.providers = SimpleNamespace()
        for key, value in cls._providers.items():
            setattr(cls.providers, key.lower(), value())
            provider = getattr(cls.providers, key)
            setattr(provider, "manager", cls)
            setattr(cls, "_instance", super().__call__(*args, **kwargs))
        super().__init__(name, bases, dct, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class ProviderInterface(metaclass=InterfaceType):
    def __init__(self):
        super().__init__()
        self._context = None
