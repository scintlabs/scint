from datetime import datetime
from deltron.data.models import Context

from deltron.data.pipeline import Message, SystemMessage
from deltron.context import Search
from deltron.utils.logger import log


class ContextBuilder:
    def __init__(self):
        self.context = Context()

    async def build(self) -> Context:
        pass
