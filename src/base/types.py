from .protocols import ProtocolType
from .lib.journal import record


class BaseType(type):
    def __new__(cls, name, bases, dct, **kwds):
        for k, v in dct.items():
            if k != "_data" and not k.startswith("__"):
                if callable(v):
                    dct[k] = record(v)
                dct["_model"][k] = v.copy()

        def build(self):
            model = {}
            for k, v in self._model.items():
                model[k] = v.model

        dct["build"] = property(build)
        return super().__new__(cls, name, bases, dct, **kwds)


class Prototype(type(ProtocolType), type(BaseType)):
    pass


class ComposerType(BaseType):
    def __new__(cls, name, bases, dct, **kwds):
        return super().__new__(cls, name, bases, dct, **kwds)
