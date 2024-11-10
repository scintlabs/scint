from typing import Any, Callable


class Maybe:
    def __init__(self, value):
        self.value = value

    def bind(self, func: Callable[[Any], "Maybe"]) -> "Maybe":
        if self.value is None:
            return Maybe(None)
        return func(self.value)

    @staticmethod
    def unit(value):
        return Maybe(value)
