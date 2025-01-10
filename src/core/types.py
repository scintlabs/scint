from __future__ import annotations

import inspect
from dataclasses import dataclass, field, fields
from typing import Any, Type, Callable, Dict, List, Optional


class BaseType(type):
    def __new__(cls, name, bases, dct, /, **kwds):
        return super().__new__(cls, name, bases, dct, **kwds)


class AspectType(BaseType):
    def __new__(cls, name, bases, dct):
        dct["_protocol_attributes"] = {
            name: value
            for name, value in dct.items()
            if not name.startswith("_") and not callable(value)
        }

        dct["_protocol_methods"] = {
            name: value
            for name, value in dct.items()
            if not name.startswith("_") and callable(value)
        }

        return super().__new__(cls, name, bases, dct)

    def __instancecheck__(cls, instance: Any) -> bool:
        for attr_name, attr_value in cls._protocol_attributes.items():
            if not hasattr(instance, attr_name):
                return False

        for method_name in cls._protocol_methods:
            if not hasattr(instance, method_name):
                return False

        return True

    def __subclasscheck__(cls, subclass: Type) -> bool:
        for attr_name in cls._protocol_attributes:
            if not hasattr(subclass, attr_name):
                return False

        for method_name in cls._protocol_methods:
            if not hasattr(subclass, method_name):
                return False

        return True


class Aspect(metaclass=BaseType):
    decorator: Callable = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.decorator is None:
            return

        for name, method in cls.__dict__.items():
            if not name.startswith("_") and (callable(method)):
                setattr(cls, name, cls.decorator(method))

    @classmethod
    def register(cls, subclass: Type) -> None:
        if not isinstance(subclass, type):
            raise TypeError("Can only register classes")
        if not cls.__subclasscheck__(subclass):
            raise TypeError(
                f"{subclass.__name__} doesn't implement the {cls.__name__} protocol"
            )


class StructType(BaseType):
    def __new__(cls, name: str, bases: tuple, namespace: dict) -> Type:
        annotations = {}
        for base in reversed(bases):
            if hasattr(base, "__annotations__"):
                annotations.update(base.__annotations__)

        annotations.update(namespace.get("__annotations__", {}))
        namespace["__annotations__"] = annotations

        for key, type_hint in annotations.items():
            if key not in namespace:
                namespace[key] = field(default=None)

        cls_obj = super().__new__(cls, name, bases, namespace)
        return dataclass(cls_obj)

    def __subclasscheck__(cls, subclass: Type) -> bool:
        required_fields = set(cls.__annotations__.keys())
        subclass_fields = set(getattr(subclass, "__annotations__", {}).keys())
        return required_fields.issubset(subclass_fields)


class Struct(metaclass=StructType):
    _parent: Optional[Struct] = field(default=None)
    _children: List[Struct] = field(default_factory=list)

    def __post_init__(self):
        for f in fields(self):
            if getattr(self, f.name) is None and f.default_factory is not None:
                setattr(self, f.name, f.default_factory())

    def add_child(self, child: Struct) -> Struct:
        child._parent = self
        self._children.append(child)
        return self

    def remove_child(self, child: Struct) -> Struct:
        if child in self._children:
            child._parent = None
            self._children.remove(child)
        return self

    @property
    def children(self) -> List[Struct]:
        return self._children

    @property
    def parent(self) -> Optional[Struct]:
        return self._parent

    @property
    def root(self) -> Struct:
        current = self
        while current.parent is not None:
            current = current.parent
        return current

    def walk(self, predicate: Optional[callable] = None):
        if predicate is None or predicate(self):
            yield self
        for child in self.children:
            yield from child.walk(predicate)

    def model(self) -> Dict[str, Any]:
        result = {}
        for f in fields(self):
            if not f.name.startswith("_"):
                value = getattr(self, f.name)
                if isinstance(value, Struct):
                    result[f.name] = value.to_dict()
                elif isinstance(value, (list, set)):
                    result[f.name] = [
                        item.to_dict() if isinstance(item, Struct) else item
                        for item in value
                    ]
                else:
                    result[f.name] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Struct:
        field_types = cls.__annotations__
        processed_data = {}

        for key, value in data.items():
            if key in field_types:
                field_type = field_types[key]
                if inspect.isclass(field_type) and issubclass(field_type, Struct):
                    processed_data[key] = field_type.from_dict(value)
                else:
                    processed_data[key] = value

        return cls(**processed_data)


class ProcessType(BaseType):
    def __new__(cls, name, bases, dct, /, **kwds):
        return super().__new__(cls, name, bases, dct, **kwds)


class MemoryType(BaseType):
    def __new__(cls, name, bases, dct, /, **kwds):
        return super().__new__(cls, name, bases, dct, **kwds)


__all__ = Aspect, Struct
