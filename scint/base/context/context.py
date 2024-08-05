import json
from types import SimpleNamespace
from typing import Any, ChainMap
from ..components.containers import Container

from ..utils import get_module, generate_id


def create_context(clsref=None, settings=None):
    class Context(
        metaclass=ContextType, kwargs={"clsref": clsref, "settings": settings}
    ):
        def __init__(self):
            pass

    return Context


class ContextType(type):
    __context__ = {}

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

    @classmethod
    def __prepare__(cls, name, bases, kwargs):
        dct = {}
        clsref = kwargs.get("clsref")
        if clsref:
            dct["identity"] = clsref
        settings = kwargs.get("settings")
        if settings:
            dct["settings"] = settings.services.as_dict()
            return dct
        global __context__
        return dct

    def __new__(cls, name, bases, dct, **kwargs):
        system = {}
        for key, value in dct["settings"].items():
            module_name = value.get("name")
            module_import_path = value.get("import_path")
            module_settings = value.get("settings")
            module = get_module(module_import_path, module_name)
            dct["system"] = system
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, *args, **kwargs):
        container = Container()
        for key, value in dct.get("system").items():
            setattr(container, key, value)
        type = dct.get("identity")
        type.services = container
        setattr(container, "context", cls)
        setattr(type, "context", cls)
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance
