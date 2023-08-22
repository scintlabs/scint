import os
from util.env import envar
from util.logging import logger

APPNAME = "scint"
APPDATA = os.path.join(envar("XDG_DATA_HOME"), APPNAME)


class State:
    def __init__(self):
        """Object for managing application state."""
        logger.info(f"Initializing application state: idle.")
        self.idle: bool = True

    def process(self):
        """State for reading and processing data."""
        logger.info(f"State change: processor.")

        if self.idle is True:
            self.idle = False

    def generate(self):
        """State for generating text and code."""
        logger.info(f"State change: generator.")
        pass

    def search(self):
        """State for searching for information."""
        pass

    def chat(self):
        """State for general discussion."""
        logger.info(f"State change: chat.")
        pass
