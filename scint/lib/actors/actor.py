from __future__ import annotations

from types import MethodType
from uuid import uuid4


from scint.lib.context import ContextProvider
from scint.lib.state import AgentState, State
from scint.lib.types.traits import Trait
from scint.lib.types.factory import Factory
from scint.lib.types.typing import _finalize_type


def init_on_enter(obj: AgentState):
    print("Entering INIT state: starting initialization...")


def init_on_exit(obj: AgentState):
    print("Exiting INIT state: finishing initialization...")


AgentState.STARTING.set_hooks(init_on_enter, init_on_exit)
# AgentState.OBSERVING.set_hooks(init_on_enter, init_on_exit)
# AgentState.RESPONDING.set_hooks(init_on_enter, init_on_exit)
# AgentState.DELEGATING.set_hooks(init_on_enter, init_on_exit)
# AgentState.STOPPING.set_hooks(init_on_enter, init_on_exit)


class ActorType(type):
    def __new__(cls, name, bases, dct, **kwargs):
        def __init__(self, *args, **kwargs):
            return self.__init_state__(*args, **kwargs)

        def __init_state__(self, *args, **kwargs):
            with self._state.state.STARTING:
                traits = []
                for a in args:
                    if isinstance(a, Trait):
                        traits.append(a)
            return

        def __init_tools__(self, *tools):
            self._tools = {} if self._tools is None else self._tools
            for k, v in self._tools.items():
                if getattr(self, k):
                    delattr(self, k)

            for t in tools:
                self._tools.update(t._tools)
                for k, v in self._tools.items():
                    func = v
                    setattr(self, k, MethodType(func, self))

        def __init_traits__(self, *args, **kwargs):
            self.traits = {}
            for a in args:
                if hasattr(a, "type") and a.type == "Trait":
                    other = self
                    a.__init_trait__(other)

        def __init_context__(self, instance):
            self._context()
            return self

        @property
        def model(self):
            return {
                "messages": [m.model for m in self.context.active.messages],
                "tools": [self.tools.model],
            }

        dct["id"] = str(uuid4())
        dct["type"] = name
        dct["model"] = model
        dct["traits"] = __init_traits__
        dct["tools"] = __init_tools__
        dct["_tools"] = {}
        dct["_state"] = State(AgentState.STARTING)
        dct["_context"] = ContextProvider()
        dct["_constructor"] = None
        dct["__init__"] = __init__
        dct["__init_state__"] = __init_state__
        dct["__init_traits__"] = __init_traits__
        dct["__init_context__"] = __init_context__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Agent(metaclass=ActorType):
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


class AgentFactory(Factory):
    Parser = ("Parser", (Agent,), {})
    Handler = ("Handler", (Agent,), {})
    Interpreter = ("Interpreter", (Agent,), {})
