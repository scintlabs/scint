from scint.base.actors.components.mixins.enum import Enumerator


def _create_enum(states):
    state = Enumerator
    for key, value in states.items():
        setattr(state, key, value)
    return state


class LoopType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return {}

    def __new__(cls, name, bases, dct, **kwds):
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance
