from types import SimpleNamespace
from typing import Protocol, runtime_checkable


@runtime_checkable
class Stateful(Protocol):
    def send(self, package: "Stateful"):
        pass


@runtime_checkable
class Trusted(Protocol):
    def route(self, package: Stateful):
        pass


@runtime_checkable
class Receiver(Protocol):
    def receive(self, package: Stateful):
        pass


class State(Stateful):
    def __init__(self):
        self.state = "Here's some state"
        self.more_state = "Some more state"
        self._private_state = "Don't look at this"
        self._more_private_state = "This is mine, go away"

    def _snapshot(self, callback):
        snapshot = {}
        for key, value in state.__dict__.items():
            if not key.startswith("_"):
                snapshot[key] = value
        return callback(snapshot)

    def send(self, trustee: Trusted, callback):
        if isinstance(trustee, Trusted):
            return self._snapshot(callback)


class Trustee(Trusted):
    def __init__(self):
        self._trustee = self

    def _snapshot(self, callback):
        return callback

    def route(self, state: Stateful):
        return state.send(self._trustee, self._snapshot)


class Entity(Receiver):
    def __init__(self):
        pass

    def receive(self, package: Stateful):
        print(package)


state = State()
router = Trustee()
delivery = router.route(state)
entity = Entity()
entity.receive(delivery)
