from enum import Enum
from types import new_class
from typing import Dict, Type


from ...util.utils import get_module
from ..types import StructType


class Resource(metaclass=StructType):
    def __init__(self, settings):
        for item in settings.get("graph"):
            name = item.get("name")
            package = item.get("package")
            params = item.get("parameters")
            ref = get_module(package, name)
            if params:
                setattr(self, name.lower(), ref(**params))
            self._load(name, package, params)

    def load(self, name, package, parameters):
        classes = self._import_modules(name, package)
        enum_members = {cls: cls(name, cls) for cls in classes}
        members = self._make_enum(name, enum_members)
        setattr(
            package,
            name.lower(),
            {k.__qualname__: self._make_factory(k, v) for k, v in members},
        )

    def import_modules(self, name, package):
        try:
            module = get_module(name, package)
            return getattr(module, "__all__")
        except ImportError as e:
            print(f"Error: '{name}' not found. {str(e)}")
            return None

    def make_factory(self, name: str, cls: type, **kwargs) -> Type:
        return new_class(name, (cls,), {**kwargs})

    def make_enum(self, name: str, members: Dict[str, Type], **kwargs):
        return Enum(name, members, **kwargs)
