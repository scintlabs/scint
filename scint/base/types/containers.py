import inspect
from types import SimpleNamespace

__all__ = "Parcel"


class ParcelType(type):
    @classmethod
    def __new__(cls, name, bases, dct):
        dct["unpack"] = cls.unpack
        if name == "Parcel" and dct.get("__module__") == __name__:
            return super().__new__(cls, name, bases, dct)
        return SimpleNamespace(**dct)

    def unpack(self, parent):
        for name, value in inspect.getmembers(self):
            if not name.startswith("__") and name != "assign_to_parent":
                if inspect.ismethod(value) or inspect.isfunction(value):
                    setattr(parent, name, value.__func__.__get__(parent))
                else:
                    setattr(parent, name, value)


class Parcel(metaclass=ParcelType):
    pass
