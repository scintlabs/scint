from __future__ import annotations

from scint.lib.util.typing import _validate_type, _finalize_type


class StructType(type):
    def __new__(cls, name, bases, dct):
        def __init__(self, *args, **kwargs):
            self._data = self.__dict__

        def __post_init__(self, **kwargs):
            for f, t in annotations.items():
                if f not in kwargs:
                    raise TypeError(f"Missing required argument: {f}")
                value = kwargs[f]
                if not _validate_type(value, t):
                    raise TypeError(f"Expected {t} for {f}, got {type(value)}")
                self._data[f] = value

        def __repr__(self):
            fields = [f"{k}={self._data[k]!r}" for k in self._data]
            return f"{self.__class__.__name__}({', '.join(fields)})"

        dct["type"] = name
        dct["__init__"] = __init__
        dct["__post_init__"] = __post_init__
        dct["__repr__"] = __repr__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Struct(metaclass=StructType):
    def __init__(self):
        print(self.__dict__)
