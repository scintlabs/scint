import os
from enum import Enum
from base.definitions.functions import LOCATOR
from util.logging import logger
from util.env import envar


class State(Enum):
    CONTROLLER = "controller"
    FINDER = "finder"
    PROCESSOR = "processor"
    TRANSFORMER = "transformer"


class StateManager:
    def __init__(self):
        self.current_state = State.CONTROLLER
        logger.info(f"Application state initialized: {self.current_state}")

    def get_state(self) -> State:
        return self.current_state

    def request_transition(self, new_state: State):
        # Validate if transition is allowed
        # Handle any cleanup for current state
        # Set the new state
        # Handle any setup for new state

        if new_state in State:
            logger.info(f"Transitioning application state to {new_state}")
            self.current_state = new_state
        else:
            logger.error(f"Invalid state: {new_state}")
            raise ValueError(f"Invalid state: {new_state}")

    def on_enter_state(self, state: State):
        if state == State.CONTROLLER:
            pass
        elif state == State.LOCATOR:
            pass
        elif state == State.PROCESSOR:
            pass
        elif state == State.TRANSFORMER:
            pass

    def on_exit_state(self, state: State):
        if state == State.CONTROLLER:
            pass
        elif state == State.FINDER:
            pass
        elif state == State.PROCESSOR:
            pass
        elif state == State.TRANSFORMER:
            pass
