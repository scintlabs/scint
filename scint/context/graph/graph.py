import numpy as np
from scint.base.models import cosine_similarity


class Graph:
    def __init__(self):
        pass

    def get_node(self, embedding, threshold=0.8):
        for key, value in self.embeddings.items():
            similarities = (key, cosine_similarity(embedding, value))

        most, highest = max(similarities, key=lambda x: x[1])  # type: ignore
        if highest >= threshold:
            return self.nodes[most], highest
        else:
            print(f"No node found with similarity above threshold {threshold}")
            return None, highest

    def get_nearest_nodes(self, embedding, n=5):
        similarities = [
            (self.nodes[loc_id], cosine_similarity(embedding, loc_embedding))
            for loc_id, loc_embedding in self.embeddings.items()
        ]
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:n]  # type: ignore

    def add_node(self, node, embedding: np.ndarray):
        id = str(node.id)
        self.nodes[id] = node
        self.embeddings[id] = embedding

    def remove_node(self, node_id: str):
        if node_id in self.nodes:
            del self.nodes[node_id]
            del self.embeddings[node_id]

    def update_node(self, node_id: str, new_embedding: np.ndarray = None):
        if node_id in self.nodes:
            if new_embedding is not None:
                self.embeddings[node_id] = new_embedding

    def get_all_nodes(self):
        return list(self.nodes.values())

    def clear(self):
        self.nodes.clear()
        self.embeddings.clear()
