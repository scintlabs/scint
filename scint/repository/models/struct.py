from validate import Validator, validated
from collections import ChainMap


# class StructType(type):
#     def __new__(cls, name, bases, dct, **kwds):
#         def __prepare__(cls, name, bases, **kwds):
#             return {"name": name, "state": Struct()}

#         def __new__(cls, name, bases, dct, **kwds):
#             def _index(self):
#                 for key, value in self.state.items():
#                     print(key)

#         def model(self):
#             dct = {}
#             for k, v in self.__dict__.items():
#                 try:
#                     dct[k] = v.model
#                 except AttributeError:
#                     if isinstance(v, list):
#                         dct[k] = [i.model for i in v]
#                     elif isinstance(v, dict):
#                         dct[k] = {k: v.__dict__ for k, v in self.__dict__.items()}
#                     elif isinstance(v, str):
#                         dct[k] = v
#             return dct

#         dct["model"] = model
#         dct["_type"] = kwds.get("type")
#         for key, value in dct.items():
#             if callable(value) and not key.startswith("__"):
#                 if callable(value):
#                     if not isinstance(value, Struct):
#                         dct[key] = Struct()

#         return super().__new__(cls, name, bases, dct)


class StructType(type):
    @classmethod
    def __prepare__(meta, clsname, bases):
        return ChainMap({})

    @staticmethod
    def __new__(meta, name, bases, methods):
        methods = methods.maps[0]
        return super().__new__(meta, name, bases, methods)

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


class Struct(metaclass=StructType):
    def __init__(self, *args, **kwargs):
        self.next = None
        self.prev = None
        for key, value in kwargs.items():
            self.add(key, value)

    def link(self, name, struct, leading=False):
        if not leading:
            self.next = Struct
            return self.next
        self.prev = struct
        return self.prev

    def add(self, name, struct):
        setattr(self, name, struct)
        return getattr(self, name)


class Structure(metaclass=StructType):
    _fields = ()
    _types = ()

    def __setattr__(self, name, value):
        if name.startswith("_") or name in self._fields:
            super().__setattr__(name, value)
        else:
            raise AttributeError("No attribute %s" % name)

    def __repr__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join(repr(getattr(self, name)) for name in self._fields),
        )

    @classmethod
    def from_row(cls, row):
        rowdata = [func(val) for func, val in zip(cls._types, row)]
        return cls(*rowdata)

    @classmethod
    def create_init(cls):
        args = ",".join(cls._fields)
        code = f"def __init__(self, {args}):\n"
        for name in cls._fields:
            code += f"    self.{name} = {name}\n"
        locs = {}
        exec(code, locs)
        cls.__init__ = locs["__init__"]

    @classmethod
    def __init_subclass__(cls):
        validate_attributes(cls)

    def validate_attributes(cls):
        validators = []
        for name, val in vars(cls).items():
            if isinstance(val, Validator):
                validators.append(val)

            elif callable(val) and val.__annotations__:
                setattr(cls, name, validated(val))

        cls._fields = tuple([v.name for v in validators])
        cls._types = tuple(
            [getattr(v, "expected_type", lambda x: x) for v in validators]
        )
        if cls._fields:
            cls.create_init()

        return cls

    def typed_structure(clsname, **validators):
        cls = type(clsname, (Structure,), validators)
        return cls
