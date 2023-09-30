from base.observability.logging import logger
from data.models.lifecycle import Lifecycle


class Coordinator:
    name: str = "Coordinator"

    def __init__(self):
        logger.info(f"Initializing {self.name}.")
        self.lifecycle = Lifecycle()
