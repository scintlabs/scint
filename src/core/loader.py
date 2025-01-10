from __future__ import annotations

from types import new_class

from src.core.types import Aspect


class Loader(Aspect):
    types = None
    aspects = None

    def load(self, name, *aspects, **kwargs):
        bases = aspects
        try:
            obj = self.create_object(name=name, bases=bases, **kwargs)
            return obj()
        except Exception as e:
            raise RuntimeError(f"Error instantiating {self.value}: {str(e)}")

    def create_object(self, name: str, /, module: str = None, **kwds):
        dct = {"__module__": __name__ if module is None else module}
        dct.update(kwds) if kwds else None
        return new_class(name, (), {}, lambda ns: ns.update(dct))
