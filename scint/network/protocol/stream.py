from typing import Dict, List


class EventStream:
    def __init__(self):
        self.events = []
        self.embeddings_projection = {}
        self.labels_projection = {}

    def append(self, event: dict):
        self.events.append(event)
        self._update_projections(event)

    def _update_projections(self, event: dict):
        if "embeddings" in event:
            self.embeddings_projection[event["id"]] = event["embeddings"]


class EmbeddingsProjection:
    def __init__(self):
        self.embeddings: Dict[str, List[float]] = {}

    def handle_event(self, event: dict):
        if event["type"] == "TextProcessed":
            self.embeddings[event["id"]] = event["embeddings"]
