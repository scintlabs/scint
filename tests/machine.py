from typing import Any, Dict
from scint.framework.models.messages import InputMessage


class Machine:
    def __init__(self):
        self.states: Dict[str, Any] = []
        self.initial: Any = None
        self.current_state: Any = None

    def add_states(self, *states):
        for state in states:
            self.states.append(state)
            if isinstance(state, Any) and self.initial is None:
                self.initial = state
                self.current_state = state

    async def input(self, message: InputMessage):
        if self.current_state is None:
            self.current_state = self.initial

        while self.current_state:
            next_state = await self.current_state.evaluate(message)
            if next_state:
                self.current_state = self.states.index(next_state)
            else:
                break
