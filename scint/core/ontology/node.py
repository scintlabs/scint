from scint.core import Core
from scint.core.ontology.status import State


class Node(Core):
    def __init__(self, id, properties, relationships, dependencies):
        super().__init__()
        self.id = id
        self.properties = properties
        self.relationships = relationships
        self.dependencies = dependencies or []
        self.state = State.LOCKED

    def unlock(self):
        if all(dep.status == State.COMPLETED for dep in self.dependencies):
            self.status = State.UNLOCKED

    def begin(self):
        if self.status == State.UNLOCKED:
            self.status = State.IN_PROGRESS

    def complete(self):
        if self.status == State.IN_PROGRESS:
            self.status = State.COMPLETED
            for node in self.next_nodes:
                node.unlock()
