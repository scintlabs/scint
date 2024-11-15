from enum import EnumMeta
from types import DynamicClassAttribute, new_class
from typing import Any, Dict

from scint.repository.models.struct import StructType


class EnumType(EnumMeta, StructType):
    def __new__(cls, name, bases, dct, **kwds):
        def name(self):
            return self._name_

        def value(self):
            return self._value_

        def __call__(cls, string_value: str, case_sensitive: bool = True):
            if not case_sensitive:
                string_value = string_value.upper()
                for member_name, member in cls._member_map_.items():
                    if member_name.upper() == string_value:
                        return member
                raise ValueError(
                    f"'{string_value}' is not a valid member of {cls.__name__}"
                )
            try:
                return cls._member_map_[string_value]
            except KeyError:
                raise ValueError(
                    f"'{string_value}' is not a valid member of {cls.__name__}"
                )

        dct["name"] = DynamicClassAttribute(name)
        dct["value"] = DynamicClassAttribute(value)
        dct["__call__"] = __call__
        return super().__new__(cls, name, bases, dct, **kwds)


def Enum(m: Dict[str, Any]):
    return new_class(
        "Enum",
        (StructType, EnumType),
        {"metaclass": EnumType},
        lambda: {"members": m},
    )


class Stimulant:
    def model(self):
        dct = {}
        for k, v in self.__dict__.items():
            try:
                dct[k] = v.model
            except AttributeError:
                if isinstance(v, list):
                    dct[k] = [i.model for i in v]
                elif isinstance(v, dict):
                    dct[k] = {k: v.__dict__ for k, v in self.__dict__.items()}
                elif isinstance(v, str):
                    dct[k] = v
        return dct

    def context(self):
        return self.model
