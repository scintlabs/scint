from base.observability.logging import logger
from base.persistence.lifecycle import LifeCycle


class Coordinator:
    name: str = "Coordinator"

    def __init__(self):
        logger.info(f"Initializing {self.name}.")
        self.lifecycle = LifeCycle()
