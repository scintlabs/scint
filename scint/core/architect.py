from scint.core import Core
from scint.core.components.compositions import Conversation
from scint.core.network.graph import Graph

from scint.core.primitives.messages import InputMessage


class Architect(Core):
    def __init__(self, context):
        super().__init__()
        self.graph = Graph()
        self.context = context
        self.context.graph = self.graph

    async def build(self):
        convo = Conversation()
        self.graph[convo.id] = convo
        return

    async def select(self, message: InputMessage):
        if self.graph.last_active_composition is None:
            await self.build()
        self.graph.last_active_composition.messages.append(message)
        return message

    async def sync(self):
        self.graph.sync_graph()
