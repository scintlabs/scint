from types import SimpleNamespace


class ComponentType(type):
    def __new__(cls, name, bases, dct, *args, **kwargs):
        dct["name"] = name.lower()
        dct["attach"] = cls.attach
        dct["unpack"] = cls.unpack
        dct["bind"] = cls.bind

        if name == "Component" and dct.get("__module__") == __name__:
            return super().__new__(cls, name, bases, dct, *args, **kwargs)
        return SimpleNamespace(**dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        for arg in args:
            setattr(instance, arg.name, arg)
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def attach(cls, binder, *args, **kwargs):
        raw_component = cls.unpack(*args, **kwargs)
        return cls.bind(binder, raw_component)

    @classmethod
    def unpack(cls, *args, **kwargs):
        data = {}
        for key, value in cls.__dict__.items():
            data[key] = value
        data.pop("__module__")
        return data

    @classmethod
    def bind(cls, binder, raw_component):
        binder(raw_component)


class Component(metaclass=ComponentType):
    pass
