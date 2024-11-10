from typing import Callable, Dict, Type

from scint.ensemble.components.enum import Enumerator
from scint.repository.models.struct import Struct, StructType


class ComposerType(StructType):
    def __new__(cls, name, bases, dct, **kwds):
        @property
        def model(self):
            dct = {}
            for k, v in self.__dict__.items():
                try:
                    dct[k] = v.model
                except AttributeError:
                    if hasattr(v, "model"):
                        setattr(dct, k, v.model)
                    elif isinstance(v, list):
                        dct[k] = [i for i in v]
                    elif isinstance(v, str):
                        dct[k] = v.model
            return dct

        def compose(self, other): ...

        def add_step(self, operation: Callable) -> Struct:
            node = Struct(operation)
            if not self.root:
                self.root = node
            return node

        def parallel(self, operation: Callable) -> Struct:
            node = self.add_step(operation)
            if self.current:
                if self.current.first_child:
                    last = self.current.first_child
                    while last.right_sibling:
                        last = last.right_sibling
                    last.right_sibling = node
                    node.left_sibling = last
                else:
                    self.current.first_child = node
                node.parent = self.current
            return node

        dct["model"] = model
        dct["root"] = None
        dct["current"] = None
        dct["compose"] = compose
        dct["add_step"] = add_step
        dct["parallel"] = parallel
        return super().__new__(cls, name, bases, dct, **kwds)


class Composer(metaclass=ComposerType):
    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings

    def compose_type(self, name: str, bases, dct, **kwargs) -> Type:
        return type(name, bases, {**dct, **kwargs})

    def compose_enum(self, name: str, members: Dict[str, Type], **kwargs):
        return Enumerator(members, **kwargs)

    def compose_process(self, process, *args, **kwargs):
        def prepare(cls, name, bases, **kwds):
            return {"process": Composer()}

        def new(cls, name, bases, dct, **kwds):
            return super().__new__(cls, name, bases, dct, **kwds)

        dct = {"__prepare__": classmethod(prepare), "__new__": new}
        return type("Process", (Composer), dct)


__all__ = Composer
