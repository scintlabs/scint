from collections import ChainMap
from importlib import import_module
from pprint import pp
from types import new_class
from typing import Type


from scint.ensemble.components.enum import Enumerator
from scint.repository.models.struct import Struct


class Conduit(Struct):
    def __init__(self, settings, *args, **kwargs):
        super().__init__()
        for k, v in settings:
            self.add_records(v.get("name"), v.get("import_path"))

    def add_records(self, name, path):
        classes = self.import_modules(name, path)
        enum_members = {cls: self.factory(name, cls) for cls in classes}
        members = Enumerator(name, enum_members).members.items()
        setattr(self, name.lower(), {k.__qualname__: v for k, v in members})

    def import_modules(self, name, path):
        return [cls for cls in getattr(import_module(path), "__all__", [])]

    def factory(self, name: str, cls: type, **kwargs) -> Type:
        return new_class(name, cls, {})

        class Context(ChainMap):
            def print(self):
                return pp(self.maps)

            def __delattr__(self, name):
                del self[name]

            def __setitem__(self, key, value):
                super().__setitem__(key, value)

            def __delitem__(self, key):
                del map[key]
