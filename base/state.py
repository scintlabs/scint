import os

from enum import Enum

from base.definitions.functions import generate_code, google_search
from util.logging import logger
from util.env import envar

APPNAME = "scint"
APPDATA = os.path.join(envar("XDG_DATA_HOME"), APPNAME)


class AppState(Enum):
    CONTROLLER = "controller"
    FINDER = "finder"
    PROCESSOR = "processor"
    GENERATOR = "generator"


class StateManager:
    """This class handles transitions between application states."""

    def __init__(self):
        self.current_state = AppState.CONTROLLER
        logger.info(f"Application state initialized: {self.current_state}")

    def get_state(self) -> AppState:
        return self.current_state

    def request_transition(self, new_state: AppState):
        # Validate if transition is allowed
        # Handle any cleanup for current state
        # Set the new state
        # Handle any setup for new state

        if new_state in AppState:
            logger.info(f"Transitioning application state to {new_state}")
            self.current_state = new_state
        else:
            logger.error(f"Invalid state: {new_state}")
            raise ValueError(f"Invalid state: {new_state}")

    def on_enter_state(self, state: AppState):
        if state == AppState.CONTROLLER:
            pass
        elif state == AppState.FINDER:
            pass
        elif state == AppState.PROCESSOR:
            pass
        elif state == AppState.GENERATOR:
            pass

    def on_exit_state(self, state: AppState):
        if state == AppState.CONTROLLER:
            pass
        elif state == AppState.FINDER:
            pass
        elif state == AppState.PROCESSOR:
            pass
        elif state == AppState.GENERATOR:
            pass
