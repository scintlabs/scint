from types import SimpleNamespace
from typing import Any, ChainMap

from scint.base.utils.attrs import get_module
from scint.base.models import generate_id
from scint import Settings

settings = Settings()
settings.load_json("settings/providers.json", "providers")


class ActorSystem:
    def __init__(self):
        self._actors = {}

    def create_actor(self, actor_class):
        actor = actor_class(id, self)
        self.actors[id] = actor
        return id

    def send_message(self, id, message: str):
        if id in self.actors:
            self.actors[id].receive(message)


class ContextType(type):
    _instance = None

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        providers = {}
        for key, value in settings.providers.as_dict().items():
            module_name = value.get("name")
            module_path = value.get("import_path")
            module = get_module(module_path, module_name)
            if module:
                providers[key] = module

        return {"_providers": providers}

    def __new__(cls, name, bases, dct, **kwargs):
        cls._id = generate_id(name)
        cls._instance = cls
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, *args, **kwargs):
        cls.providers = SimpleNamespace()
        try:
            for key, value in cls._providers.items():
                print(key)
                print(value)
                setattr(cls.providers, key.lower(), value())
                provider = getattr(cls.providers, key)
                setattr(cls, "_instance", super().__call__(*args, **kwargs))
        except Exception as e:
            print(f"Error processing intelligence request: {e}")

        super().__init__(name, bases, dct, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class Context(metaclass=ContextType):
    def __init__(self):
        super().__init__()
        self._context = {"global": {}, "actors": {}}

    def set_actor_context(self, id, key: str, value: Any):
        if id not in self._context["actors"]:
            self._context["actors"][id] = {}
        self._context["actors"][id][key] = value

    def get_actor_context(self, id, key: str, default=None):
        return self._context["actors"].get(id, {}).get(key, default)

    def get_full_context(self, id):
        context = self._context["global"].copy()
        context.update(self._context["actors"].get(id, {}))
        return context


class DeepChainMap(ChainMap):
    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)
