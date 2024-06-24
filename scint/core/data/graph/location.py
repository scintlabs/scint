from uuid import uuid4

import numpy as np


from scint.core.data.containers.collections import Collection, Messages
from scint.core.data.containers.blocks import Embedding
from scint.core.data.metadata import gather_metadata
from scint.support.logging import log
from scint.support.types import List, Union
from scint.support.utils import cosine_similarity


class Location:
    def __init__(self):
        self.id = str(uuid4())
        self.weight = 0.0
        self.density = 0.0
        self.collections = []
        self.waypoints = []
        self.embedding = property(self._embedding)

    def anchor(self, context):
        self.context = context

    def release(self, context):
        self.context = None

    def get_collection(self, collection):
        if collection in self.collections:
            return self.collections[collection]

    def _embedding(self):
        iterable = self.__dict__

        def weight(embedding):
            total_weight = sum(self.collections.values())
            weighted_embeddings = [
                embedding * (self.connections[key] / total_weight)
                for key, embedding in embedding.items()
            ]
            return np.sum(weighted_embeddings, axis=0)

        weighted_embeddings = gather_metadata(iterable, list(), callback=weight)
        return (
            np.mean(np.array(weighted_embeddings), axis=0)
            if weighted_embeddings
            else None
        )
