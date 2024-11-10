from enum import EnumMeta
from types import DynamicClassAttribute

from scint.repository.models.struct import StructType


class EnumType(EnumMeta, StructType):
    def __init__(self, __o: object):
        super().__init__(__o)
        self.members = None
        self.TEXT = None
        self.TEXT = None

    def __new__(cls, name, bases, dct, **kwds):
        def name(self):
            return self._name_

        def value(self):
            return self._value_

        @property
        def model(self):
            return {k: v.__dict__ for k, v in self.__dict__}

        @property
        def context(self, *args, **kwargs):
            return self.model

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
        dct["model"] = model
        dct["__call__"] = __call__
        return super().__new__(cls, name, bases, dct, **kwds)


def Enumerator(*args, **kwargs) -> EnumType:
    return type("Enum", (EnumType,), kwargs)
