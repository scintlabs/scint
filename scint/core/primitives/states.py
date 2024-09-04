from typing import List

from scint.core.primitives import Primitive
from scint.core.primitives.instructions import Transition
from scint.core.primitives.messages import InputMessage


class State(Primitive):
    def __init__(self, name: str, behavior=None, transitions=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.behavior = behavior
        self.transitions: List[Transition] = transitions

    async def evaluate(self, message: InputMessage):
        if self.behavior:
            await self.behavior.evaluate(message)
        for transition in self.transitions:
            if await transition.can_transition(message):
                return transition.target
        return None
