import os
import uuid
from datetime import datetime

from services.logger import log


class File:
    def __init__(self, filename):
        log.info(f"Created file: {filename}.")

        self.id = File._generate_id()
        self.date: datetime = datetime.now()

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())
