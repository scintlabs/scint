import operator
from functools import reduce
from scint.core.utils.logger import logger


__all__ = "context", "App", "Core"


class NetworkMux(dict):
    def __init__(self, objs):
        dict.__init__(self)
        for alias, obj in objs:
            self[alias] = obj

    def __call__(self, *args, **kwargs):
        return self.__class__(
            [(alias, obj(*args, **kwargs)) for alias, obj in self.items()]
        )

    def __nonzero__(self):
        return reduce(operator.and_, self.values(), 1)

    def __getattr__(self, name):
        try:
            return dict.__getattribute__(self, name)
        except Exception as e:
            e
            return self.__class__(
                [(alias, getattr(obj, name)) for alias, obj in self.items()]
            )

    def create(self, other):
        name = type(other).__name__.lower()
        self[name] = other


class NetworkDict(dict):
    def __init__(self):
        super().__init__()

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        return self

    def __setattr__(self, name, value):
        self[name] = value

    def mux(self, objects):
        return NetworkMux([objects])

    def insert(self, other):
        name = type(other).__name__.lower()
        setattr(self._network, name, object)

    def locate(self, *args, **kwargs):
        pass


class NetworkType(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return {"_network": NetworkDict()}

    def __new__(cls, name, bases, dct):
        for key, value in dct.items():
            if callable(value):
                dct[key] = logger(value)

        def __enter__(self, *args, **kwargs):
            return self.network(*args, **kwargs)

        def __exit__(self, exc_type, exc_val, exc_tb):
            return

        async def __aenter__(self):
            return self.__enter__()

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return self.__exit__(exc_type, exc_val, exc_tb)

        def network(self, *args, **kwargs):
            return self._network

        dct["network"] = network
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, **kwds):
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class Network(metaclass=NetworkType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for name, value in kwargs.items():
            setattr(self, name, value)

    def __get__(self, obj, objtype=None):
        with self.network() as network:
            if obj is None:
                return network
        return obj.__dict__.get(self.name)

    def __set__(self, key, value):
        with self.network() as network:
            network[key] = value
