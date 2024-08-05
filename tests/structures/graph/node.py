from uuid import uuid4

import numpy as np


class Node:
    def __init__(self):
        self.id = str(uuid4())
        self.weight = 0.0
        self.density = 0.0
        self.collections = []
        self.edges = []
        self.embedding = property(self._embedding)

    def _embedding(self):
        iterable = self.__dict__

        def weight(embedding):
            total_weight = sum(self.collections.values())
            weighted_embeddings = [
                embedding * (self.connections[key] / total_weight)
                for key, embedding in embedding.items()
            ]
            return np.sum(weighted_embeddings, axis=0)
