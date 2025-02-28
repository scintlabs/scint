from src.types.typing import Any, List


class Requires:
    def __init__(self, *requirements: List[Any]):
        self.name = "_requires"
        self.requirements = list(requirements)

    def __set_name__(self, instance, owner):
        self.owner = owner

    def __get__(self, instance, owner):
        if instance is not None:
            for obj in self.requirements:
                pass
        return self
