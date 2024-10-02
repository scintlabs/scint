from typing import Dict, List

from scint.framework.collections.collection import Collection
from scint.framework.utils.helpers import cosine_similarity


class Domain(Collection):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.data = None
        self.id: int = None
        self.embedding: List[float] = []
        self.collections: Dict[str, Collection] = {}

    def add_collection(self, collection: Collection):
        similarity = cosine_similarity(self.embedding, collection.embedding)
        threshold = 0.7
        if similarity >= threshold or not self.collections:
            self.collections[collection.name] = collection
            self.embedding = self.calculate_embedding()
        else:
            pass

    def calculate_embedding(self) -> List[float]:
        embeddings = [collection.embedding for collection in self.collections.values()]
        if not embeddings:
            return [0.0] * 1536
        averaged_embedding = [sum(values) / len(values) for values in zip(*embeddings)]
        return averaged_embedding
