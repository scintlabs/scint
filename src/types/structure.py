from __future__ import annotations

from types import MethodType, FunctionType
from typing import Any, List, Optional

from src.types.models import Context, Model
from src.types.typing import _finalize_type


class Property(Model):
    type: str
    name: str
    description: str
    items: Optional[List[Any]] = None

    @property
    def model(self):
        prop = {"type": self.type, "description": self.description}
        if self.type == "enum":
            prop["enum"] = self.items
        elif self.type == "array":
            prop["array"] = self.items
        return prop


class Properties(Model):
    name: Optional[str] = None
    description: Optional[str] = None
    properties: List[Property] = []

    @property
    def model(self):
        return {
            "type": "object",
            "properties": {p.name: p.model for p in self.parameters},
            "additionalProperties": False,
            "required": [p.name for p in self.parameters],
        }


class Requirements:
    def __init__(self, *requirements: List[Any]):
        self.name = "_requires"
        self.requirements = list(requirements)

    def __set_name__(self, instance, owner):
        self.owner = owner

    def __get__(self, instance, owner):
        if instance is not None:
            for obj in self.requirements:
                if not hasattr(instance, obj):
                    raise AttributeError(f"{self.name} requires {obj}.")
        return self


class TraitType(type):
    def __new__(cls, name, bases, dct):
        @staticmethod
        def __init_trait__(other):
            for k, v in dct.items():
                if not k.startswith("_") and isinstance(v, (FunctionType, MethodType)):
                    func = v
                    func.trait = name
                    meth = MethodType(v, other)
                    setattr(other, k, meth)

        dct["name"] = name
        dct["__init_trait__"] = __init_trait__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class StructType(type):
    def __new__(cls, name, bases, dct, traits=(), **kwargs):
        def __init__(self, traits: List[type] = None):
            all_traits = []
            if hasattr(self, "__class_traits__"):
                all_traits.extend(self.__class_traits__)
                all_traits.extend(traits) if traits is not None else None

            for t in all_traits:
                t.__init_trait__(self)

        keys_to_remove = []

        for k, v in dct.items():
            if k.startswith("_"):
                continue
            if isinstance(v, (FunctionType, MethodType)):
                keys_to_remove.append(k)
        for k in keys_to_remove:
            dct.pop(k)

        def update(self, *args):
            self.context.update(*args)

        async def invoke(self, schema=None):
            from importlib import import_module

            module = import_module("src.types.agents")
            Agent = getattr(module, "Agent")
            agent = Agent(schema=None, context=self.context)
            return await agent.evaluate()

        dct["__init__"] = __init__
        dct["__class_traits__"] = traits
        dct["update"] = update
        dct["invoke"] = invoke
        dct = _finalize_type(name, bases, dct)
        new_cls = super().__new__(cls, name, bases, dct)
        return new_cls


class Trait(metaclass=TraitType):
    requirements: Requirements = Requirements()


class Struct(metaclass=StructType, traits=None):
    properties: Properties = Properties()
    context: Context = Context()
