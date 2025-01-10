from __future__ import annotations

from typing import Any, Dict

from src.core.types import Aspect


class Metadata(Aspect):
    @property
    def labels(self):
        if len(self.messages) > 0:
            return [m.labels for m in self.messages if m.labels]

    @property
    def annotations(self):
        if len(self.messages) > 0:
            return " ".join([m.annotation for m in self.messages if m.annotation])

    @property
    def embeddings(self):
        if len(self.messages) > 0:
            return [m.embedding for m in self.messages if m.embedding]

    @classmethod
    def arguments(cls):
        return {k: None for k in cls.model_fields.keys()}

    @classmethod
    def create(cls, metadata: Dict[str, Any]):
        required_args = {k for k, v in cls.model_fields.items() if v.is_required}
        return cls(**metadata) if all(k in metadata for k in required_args) else None
