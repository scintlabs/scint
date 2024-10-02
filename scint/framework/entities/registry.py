from enum import Enum
from importlib import import_module

from scint.framework.types.base import BaseType


class Registry(metaclass=BaseType):
    def __init__(self, context, name, module_paths):
        self.name = name
        self.items = self._build(name, module_paths)
        self.list_classes()

    def list_classes(self):
        return {self.name: [item.name for item in self.items]}

    def create_factory(self, class_name: str, *args, **kwargs):
        def factory(object, **arguments):
            return object(**arguments)

        object = self.factories.get(class_name)
        if object:
            return factory(*args, **kwargs)
        else:
            raise ValueError(f"No factory found for {class_name}")

    def _build(self, name, module_paths):
        classes = self._import(module_paths)
        return Enum(name, {c.name.capitalize(): c for c in classes})

    def _import(self, module_paths):
        try:
            classes = []
            for path in module_paths:
                module = import_module(path)
                classes.extend(getattr(module, "__all__"))
            return classes
        except ImportError as e:
            print(f"Error: '{self.name}' not found. {str(e)}")
            return None
