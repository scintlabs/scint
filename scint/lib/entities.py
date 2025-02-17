from __future__ import annotations

from uuid import uuid4

from scint.lib.context import Contextual
from scint.lib.common.state import Stateful, State
from scint.lib.common.tools import Tools
from scint.lib.common.traits import Traits, Trait
from scint.lib.common.typing import Constructor, _finalize_type


def init_on_enter(obj: Stateful):
    print("Entering INIT state: starting initialization...")


def init_on_exit(obj: Stateful):
    print("Exiting INIT state: finishing initialization...")


State.INIT.set_hooks(init_on_enter, init_on_exit)
State.PARSING.set_hooks(init_on_enter, init_on_exit)
State.INTERPRETING.set_hooks(init_on_enter, init_on_exit)
State.PROCESSING.set_hooks(init_on_enter, init_on_exit)
State.COMPOSING.set_hooks(init_on_enter, init_on_exit)


class EntityType(type):
    def __new__(cls, name, bases, dct, **kwargs):
        def __init__(self, *args, **kwargs):
            return self.__init_state__(*args, **kwargs)

        def __init_state__(self, *args, **kwargs):
            with self._state.state.INIT:
                traits = []
                for a in args:
                    if isinstance(a, Trait):
                        traits.append(a)

            return

        def __init_traits__(self, *traits):
            list(traits).extend(self._defaults)
            return self._traits(*traits)

        def __init_context__(self, instance):
            self._context()
            return self

        @property
        def model(self):
            return {
                "messages": [m.model for m in self.context.messages],
                "tools": [self.tools.model],
            }

        dct["id"] = str(uuid4())
        dct["type"] = name
        dct["model"] = model
        dct["_state"] = Stateful(State.INIT)
        dct["_traits"] = Traits
        dct["_defaults"] = []
        dct["_context"] = Contextual()
        dct["_tools"] = Tools()
        dct["_constructor"] = "EntityConstructor"
        dct["__init__"] = __init__
        dct["__init_state__"] = __init_state__
        dct["__init_traits__"] = __init_traits__
        dct["__init_context__"] = __init_context__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Entity(metaclass=EntityType):
    @property
    def state(self):
        return self._state

    @property
    def traits(self):
        return self._traits

    @property
    def context(self):
        return self._context

    @property
    def tools(self):
        return self._tools

    @property
    def new(self, *args, **kwargs):
        return self._constructor


class Parser(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Handler(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Interpreter(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Prism(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EntityConstructor(Constructor):
    Prism = ("Parser", (Parser,), {})
    Parser = ("Parser", (Parser,), {})
    Handler = ("Handler", (Handler,), {})
    Interpreter = ("Interpreter", (Interpreter,), {})
