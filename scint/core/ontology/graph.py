from typing import Dict


from scint.core.ontology.status import State
from scint.core.components import Composition
from scint.core.primitives.block import Link
from scint.services.persistence import Persistence


class Graph:
    def __init__(self):
        self.nodes = {}
        self.current_path = []

    def add_node(self, node):
        self.nodes[node.id] = node

    def connect_nodes(self, from_node_id: str, to_node_id: str):
        from_node = self.nodes.get(from_node_id)
        to_node = self.nodes.get(to_node_id)
        if from_node and to_node:
            from_node.add_next_node(to_node)
            to_node.dependencies.append(from_node)

    def start_path(self, start_node_id: str):
        start_node = self.nodes.get(start_node_id)
        if start_node and start_node.status == State.UNLOCKED:
            self.current_path = [start_node]
            start_node.mark_in_progress()

    def progress_to_next_node(self):
        if self.current_path:
            current_node = self.current_path[-1]
            current_node.complete()
            if current_node.next_nodes:
                next_node = current_node.next_nodes[0]
                self.current_path.append(next_node)
                next_node.mark_in_progress()

    def get_current_node(self):
        if self.current_path:
            return self.current_path[-1]
        return None


class OldGraph(Composition, Persistence):
    def __init__(self):
        super().__init__()
        self.links: Dict[str, Link] = {}
        self._compositions: Dict[str, Composition] = {}
        self.last_active_composition: Composition = None

    @property
    def compositions(self) -> Dict[str, Composition]:
        return self._compositions

    @compositions.setter
    def compositions(self, value: Dict[str, Composition]):
        self._compositions = value
        if value:
            self.last_active_composition = next(reversed(value.values()))

    def update_composition(self, key: str, composition: Composition):
        self._compositions[key] = composition
        self.last_active_composition = composition

    def __setitem__(self, key: str, value: Composition):
        self.update_composition(key, value)

    def __getitem__(self, key: str) -> Composition:
        return self._compositions[key]
