from scint.ensemble.traits.base import Trait


class Descriptor(Trait):
    def __set_name__(name):
        pass

    def __getattr__(self, name):
        pass

    def __setattr__(self, name, value):
        pass


class ComponentDescriptor(Trait):
    def __init__(self):
        self.components = None
        self.components = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(self.components, self.name, None)

    def __set__(self, component, value):
        setattr(self.components, self.name, value)


class StateDescriptor(Trait):
    def __getattr__(self, name):
        return getattr(self.state, name)

    def __setattr__(self, name, value):
        if name == "state":
            super().__setattr__(name, value)
        else:
            setattr(self.state, name, value)
