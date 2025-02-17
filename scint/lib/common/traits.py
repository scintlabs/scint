from __future__ import annotations

from types import FunctionType, MethodType

from scint.lib.common.typing import _finalize_type


class TraitType(type):
    def __new__(cls, name, bases, dct):
        functions = {}

        for k, v in dct.items():
            if not k.startswith("_") and isinstance(v, (FunctionType, MethodType)):
                functions[k] = v
            if name == "__init_trait__":
                functions[k] = v

        def __init_trait__(instance):
            for k, v in dct.items():
                if k.startswith("_init_"):
                    getattr(instance, k)()

        dct["_functions"] = functions
        dct["__init_trait__"] = __init_trait__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Trait(metaclass=TraitType):
    def __init__(self): ...


class Traits:
    def __init__(self, *traits):
        self.name = "_traits"
        self.original_traits = list(traits)
        self.current_traits = []
        self._instance = None
        self._initialized = False

    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if not hasattr(instance, f"_{self.name}"):
            self._instance = instance
            instance_traits = Traits()
            instance_traits._instance = instance
            setattr(instance, self.name, instance_traits)
            return instance_traits

        return getattr(instance, self.name)

    def __call__(self, *traits):
        self.current_traits = list(traits)
        if self._instance:
            self._init_instance()
        return self

    def _init_instance(self):
        if self._initialized:
            return

        for trait in self.current_traits:
            print(trait)
            for k, v in trait._functions.items():
                if callable(v):
                    method = MethodType(v, self._instance)
                    setattr(self._instance, k, method)

        self._initialized = True
