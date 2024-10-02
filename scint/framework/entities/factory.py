from scint.framework.components import Component
from scint.framework.types.base import BaseType


class Factory(metaclass=BaseType):
    def __init__(self, context, *args, **kwargs):
        self.compositions = {}
        for item in args:
            setattr(self, type(item).__name__.lower(), item)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create_composition(self, kind, *args, **kwargs):
        composition = kind
        self.compositions[composition.id] = composition
        return self.compositions[composition]

    def get_composition(self, composition_id):
        if composition_id in self.compositions.keys():
            return self.compositions[composition_id]

    def update_composition(self, composition, *args, **kargs):
        for arg in args:
            print(composition)
            print(arg)

    async def compose(self, composition):
        components = {}
        results = await self.search.results(self.context, composition)
        for result in results:
            result.pop("id")
            component = Component(**result)
            components[type(component).__name__] = component
        return composition.update(components)
