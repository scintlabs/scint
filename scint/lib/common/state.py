from enum import Enum
from scint.lib.common.typing import List, Optional


class StateTransitionError(Exception):
    pass


class State(Enum):
    INIT = ("INIT", "READY")
    READY = ("READY", None)
    PARSING = ("PARSING", "INTERPRETING")
    INTERPRETING = ("INTERPRETING", "PROCESSING")
    PROCESSING = ("PROCESSING", "COMPOSING")
    COMPOSING = ("COMPOSING", "READY")
    HALT = ("HALTING", None)

    def __init__(self, state_name: str, default_next: Optional[str]):
        self.state_name = state_name
        self.default_next = default_next
        self.on_enter = lambda obj: None
        self.on_exit = lambda obj: None

    def set_hooks(self, on_enter, on_exit) -> None:
        self.on_enter = on_enter
        self.on_exit = on_exit


class BoundStateContextManager:
    def __init__(self, obj: "Stateful", state: State):
        self.obj = obj
        self.state = state

    def __enter__(self):
        if self.obj.current_state != self.state:
            self.obj.transition_to(self.state)
        self.state.on_enter(self.obj)
        return self.obj

    def __exit__(self, exc_type, exc_value, traceback):
        self.state.on_exit(self.obj)
        if self.state.default_next:
            next_state = State[self.state.default_next]
            self.obj.transition_to(next_state)
        return False


class StateProxy:
    def __init__(self, obj: State):
        self.obj = obj

    def __getattr__(self, name: str) -> BoundStateContextManager:
        try:
            state = State[name]
        except KeyError:
            raise AttributeError(f"No such state: {name}")
        return BoundStateContextManager(self.obj, state)


class Stateful:
    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.state_history: List[State] = [initial_state]

    @property
    def state(self) -> StateProxy:
        return StateProxy(self)

    def transition_to(self, new_state: State):
        print(
            f"Transitioning from {self.current_state.state_name} to {new_state.state_name}"
        )
        self.current_state = new_state
        self.state_history.append(new_state)
