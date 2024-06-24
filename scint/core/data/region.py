from uuid import uuid4
from scint.core.data.graph.location import Location
from scint.support.logging import log
from scint.support.utils import cosine_similarity
from typing import Dict, List, Tuple
import numpy as np


class Region:
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.embeddings: Dict[str, np.ndarray] = {}

    def get_location(self, embedding, threshold=0.8):
        for key, value in self.embeddings.items():
            similarities = (key, cosine_similarity(embedding, value))

        most, highest = max(similarities, key=lambda x: x[1])  # type: ignore
        if highest >= threshold:
            return self.locations[most], highest
        else:
            log.info(f"No location found with similarity above threshold {threshold}")
            return None, highest

    def get_nearest_locations(self, embedding, n=5):
        similarities = [
            (self.locations[loc_id], cosine_similarity(embedding, loc_embedding))
            for loc_id, loc_embedding in self.embeddings.items()
        ]
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:n]

    def add_location(self, location: Location, embedding: np.ndarray):
        location_id = str(location.id)
        self.locations[location_id] = location
        self.embeddings[location_id] = embedding
        log.info(f"Added location {location_id} to the region")

    def remove_location(self, location_id: str):
        if location_id in self.locations:
            del self.locations[location_id]
            del self.embeddings[location_id]
            log.info(f"Removed location {location_id} from the region")

    def update_location(self, location_id: str, new_embedding: np.ndarray = None):
        if location_id in self.locations:
            if new_embedding is not None:
                self.embeddings[location_id] = new_embedding
            log.info(f"Updated location {location_id}")
        else:
            log.warning(f"Location {location_id} not found in the region")

    def get_all_locations(self) -> List[Location]:
        return list(self.locations.values())

    def clear(self):
        self.locations.clear()
        self.embeddings.clear()
        log.info("Cleared all locations from the region")


region = Region()
