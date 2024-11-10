from dataclasses import Field, dataclass, fields, is_dataclass
from enum import Enum
from functools import wraps
from typing import Any, Union, get_args, get_origin, get_type_hints


class TypeError(Exception): ...


@dataclass
class Model:
    def validate(self, dc) -> type[Enum]:
        class Validator:

            def __init__(self, field: Field, type_hint: type):
                self.field = field
                self.type_hint = type_hint

            def __call__(self, val: Any) -> bool:
                if not self._validate(val):
                    raise TypeError(
                        f"Invalid type for {self.field.name}: "
                        f"expected {self.type_hint}, got {type(val)}"
                    )
                return True

            def _validate(self, val: Any) -> bool:
                if get_origin(self.type_hint) is Union:
                    return any(isinstance(val, t) for t in get_args(self.type_hint))
                elif get_origin(self.type_hint) is list:
                    v = get_args(self.type_hint)[0]
                    return isinstance(val, list) and all(isinstance(k, v) for k in val)
                return isinstance(val, self.type_hint)

            def __repr__(self) -> str:
                return f"Validator({self.field.name}: {self.type_hint})"

        if not is_dataclass(dc):
            raise TypeError(f"{dc.__name__} must be a dataclass")

        self._validate = Enum(
            dc.__name__ + "Enum",
            {f.name: Validator(f, get_type_hints(dc)[f.name]) for f in fields(dc)},
        )
        original_init = dc.__init__

        @wraps(original_init)
        def type_checked_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            for field in fields(dc):
                value = getattr(self, field.name)
                getattr(self._validate, field.name).value(value)

        dc.__init__ = type_checked_init
        return self._validate

    @classmethod
    def Bundle(cls, title, description, collection_data):
        pass

    @classmethod
    def select(cls, param):
        pass
