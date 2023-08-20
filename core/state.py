import os


class State:
    def __init__(self):
        """Object for managing application state."""
        self.active: bool = True
        self.DATA_HOME = os.environ["XDG_DATA_HOME"]
        self.APPDATA = os.path.join(self.DATA_HOME, "scint")

    def process(self):
        """State for reading and processing data."""
        if self.active is False:
            self.active = True

    def generate(self):
        """State for generating text and code."""
        pass

    def search(self):
        """State for searching for information."""
        pass

    def chat(self):
        """State for general discussion."""
        pass
