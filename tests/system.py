from typing import NamedTuple, Tuple


class TraitType(type):
    def __new__(cls, name, bases, dct, **kwds):
        depth = 1
        for base in bases:
            if getattr(base, "__is_trait__", False):
                base_depth = getattr(base, "__trait_depth__", 1)
                depth = max(depth, base_depth + 1)
        if depth > 3:
            raise TypeError(
                f"Traits can only be subclassed three times (attempted depth {depth}) in {name}"
            )

        # allowed_keys = "requires"
        # for attr, value in dct.items():
        #     if (
        #         attr not in allowed_keys
        #         or not attr.startswith("__")
        #         or not callable(value)
        #     ):
        #         raise TypeError(f"Trait attribute '{attr}' must be a function.")

        cls = super().__new__(cls, name, bases, dict(dct))
        cls.__trait_depth__ = depth
        cls.__is_trait__ = True
        return cls


class BaseTrait(metaclass=TraitType):
    requires: Tuple[str, ...]


class Trait(BaseTrait):
    requires: Tuple[str, ...]


class Property:
    def __init__(self, f):
        if not callable(f):
            raise TypeError("Property must wrap a callable")
        self.f = f
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class StructMeta(type):
    def __new__(metacls, name, bases, namespace, **kwargs):
        properties = {}
        for attr, value in list(namespace.items()):
            if attr.startswith("__") and attr.endswith("__"):
                continue
            if not isinstance(value, Property):
                raise TypeError(
                    f"Struct attribute '{attr}' must be a Property instance"
                )
            properties[attr] = value
        namespace["__slots__"] = tuple(properties.keys())
        cls = super().__new__(metacls, name, bases, dict(namespace))
        cls._properties = properties
        return cls


class Struct(metaclass=StructMeta):
    def __init__(self, **kwargs):
        for key in kwargs:
            if key not in self.__slots__:
                raise TypeError(f"Unexpected field: {key}")
        for prop in self.__slots__:
            if prop in kwargs:
                setattr(self, prop, kwargs[prop])
            else:
                setattr(self, prop, None)


class Implements:
    def __init__(self, *traits):
        for trait in traits:
            if not getattr(trait, "__is_trait__", False):
                raise TypeError(f"{trait} is not a valid Trait")
        self.traits = traits

    def __set_name__(self, owner, name):
        if not issubclass(owner, Struct):
            raise TypeError("Implements can only be used in subclasses of Struct")
        for trait in self.traits:
            for req in trait.requires:
                attr = getattr(owner, req, None)
                if attr is None or not isinstance(attr, Property):
                    raise TypeError(
                        f"Struct '{owner.__name__}' does not implement required property "
                        f"'{req}' for trait '{trait.__name__}'"
                    )
            for attr_name, attr_value in trait.__dict__.items():
                if attr_name.startswith("__") and attr_name.endswith("__"):
                    continue
                if attr_name == "requires":
                    continue
                if hasattr(owner, attr_name):
                    raise TypeError(
                        f"Struct '{owner.__name__}' already has attribute '{attr_name}' defined; "
                        f"cannot override with trait '{trait.__name__}'"
                    )
                setattr(owner, attr_name, attr_value)
        setattr(owner, name, self)


class DataTrait(Trait):
    requires = ("schema",)

    def process(self):
        return f"Processing {self.data}"


class MyStruct(Struct):
    data = Property(lambda self: None)
    implements = Implements(DataTrait)


if __name__ == "__main__":
    s = MyStruct(data=42)
    print(s.process())
