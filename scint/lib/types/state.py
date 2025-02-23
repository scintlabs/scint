from __future__ import annotations

from enum import Enum
from typing import Type, TypeVar, Optional, Any


T = TypeVar("T")
U = TypeVar("U")


def starting_enter(obj: State):
    print("Entering INIT state: starting initialization...")


def starting_exit(obj: State):
    print("Exiting INIT state: finishing initialization...")


# State.STARTING.set_hooks(starting_enter, starting_exit)
# PrototypeState.OBSERVING.set_hooks(init_on_enter, init_on_exit)
# PrototypeState.RESPONDING.set_hooks(init_on_enter, init_on_exit)
# PrototypeState.DELEGATING.set_hooks(init_on_enter, init_on_exit)
# PrototypeState.STOPPING.set_hooks(init_on_enter, init_on_exit)


# def get_context() -> StateMonad[StateContext]:
#     return StateMonad(lambda context: (context, context))


# def set_context(new_context: StateContext) -> StateMonad[None]:
#     return StateMonad(lambda _: (None, new_context))


# def modify_context(f: Callable[[StateContext], StateContext]) -> StateMonad[None]:
#     return StateMonad(lambda context: (None, f(context)))


class StateHooks:
    def __init__(self, instance):
        instance.state.STARTING.set_hooks(self.starting_in, self.starting_out)
        instance.state.WAITING.set_hooks(self.waiting_in, self.waiting_out)
        instance.state.OBSERVING.set_hooks(self.waiting_in, self.waiting_out)
        instance.state.STOPPING.set_hooks(self.waiting_in, self.waiting_out)

    def starting_in(owner: Any, state: State):
        print(f"Starting {owner.type}...")

    def starting_out(owner: Any, state: State):
        print(f"Started {owner.type}.")

    def waiting_in(owner: Any, state: State):
        print(f"{owner.type} is waiting...")

    def waiting_out(owner: Any, state: State):
        print(f"Starting {owner.type}...")

    def observing_in(owner: Any, state: State):
        print(f"Starting {owner.type}...")

    def observing_out(owner: Any, state: State):
        print(f"Starting {owner.type}...")

    def stopping_in(owner: Any, state: State):
        print(f"Starting {owner.type}...")

    def stopping_out(owner: Any, state: State):
        print(f"Starting {owner.type}...")


class State(Enum):
    STARTING = ("STARTING", None)
    OBSERVING = ("OBSERVING", None)
    RESPONDING = ("RESPONDING", None)
    PROCESSING = ("PROCESSING", None)
    STOPPING = ("STOPPING", None)

    def __init__(self, owner: Type, state: str, next: Optional[str] = None):
        self.state = state
        self.next = next
        self.on_enter = lambda obj: None
        self.on_exit = lambda obj: None

    def set_hooks(self, on_enter, on_exit) -> None:
        self.on_enter = on_enter
        self.on_exit = on_exit


# class StateContextManager:
#     def __init__(self, obj: Stateful, state: State):
#         self.obj = obj
#         self.state = state

#     def __enter__(self):
#         if self.obj.current != self.state:
#             self.obj.transition_to(self.state)
#         self.state.on_enter(self.obj)
#         return self.obj

#     def __exit__(self, exc_type, exc_value, traceback):
#         self.state.on_exit(self.obj)
#         if self.state.next:
#             next_state = State[self.state.next]
#             self.obj.transition_to(next_state)
#         return False


# class StateProxy:
#     def __init__(self, obj: State):
#         self.obj = obj

#     def __getattr__(self, name: str) -> StateContextManager:
#         try:
#             state = State[name]
#         except KeyError:
#             raise AttributeError(f"No such state: {name}")
#         return StateContextManager(self.obj, state)


# class Stateful:
#     def __init__(self, initial: State):
#         self.current = initial
#         self.history: List[State] = [self.current]

#     @property
#     def state(self):
#         return StateProxy(self)

#     def transition_to(self, new_state: State):
#         print(f"Transitioning from {self.current.state} to {new_state.state}")
#         self.current = new_state
#         self.history.append(new_state)


# class StateContext(Model):
#     current_state: str
#     previous_state: Optional[str]
#     data: Dict[str, Any]


# class StateMonad(Generic[T]):
#     def __init__(self, computation: Callable[[StateContext], tuple[T, StateContext]]):
#         self.computation = computation

#     @staticmethod
#     def unit(value: T) -> StateMonad[T]:
#         return StateMonad(lambda context: (value, context))

#     def bind(self, f: Callable[[T], StateMonad[U]]) -> StateMonad[U]:
#         def new_computation(context: StateContext) -> tuple[U, StateContext]:
#             value, new_context = self.computation(context)
#             return f(value).computation(new_context)

#         return StateMonad(new_computation)

#     def run(self, context: StateContext) -> tuple[T, StateContext]:
#         return self.computation(context)
