from __future__ import annotations

from typing import List

from scint.lib.types import Struct, Trait
from scint.lib.util.utils import cosine_similarity
from scint.lib.util.intelligence import generate_embedding


EMBEDDING_THRESHOLD = 6
SIMILARITY_THRESHOLD = 0.8
SPLIT_MESSAGE_COUNT = 2


class Classifiable(Trait):
    def current_metadata(self):
        self.keywords = [", ".join(m.keywords) for m in self.messages]
        content = ["".join(b.text for b in (m for m in self.messages))]
        self.embeddings.append(generate_embedding(content))

    def update_metadata(self):
        self.keywords = [", ".join(getattr(m, "keywords", [])) for m in self.messages]

        content = [
            "".join(getattr(b, "text", "") for b in getattr(m, "content", []))
            for m in self.messages
        ]
        new_embedding = generate_embedding(content)

        if self.embeddings:
            previous_embedding = self.embeddings[-1]
            similarity = cosine_similarity(previous_embedding, new_embedding)
            if similarity < SIMILARITY_THRESHOLD:
                self.split_thread()

        self.embeddings.append(new_embedding)


class Classifier(Struct):
    traits: List[Trait] = [Classifiable]
