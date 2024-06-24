from datetime import time
import traceback
from typing import Self
from uuid import uuid4
from enum import Enum, auto
from abc import ABC, abstractmethod

import numpy as np


from scint.core.context import Context, State
from scint.core.data.region import region
from scint.core.data.graph.location import Location
from scint.core.data.containers.collections import Messages, Prompts, Functions
from scint.intelligence.provider import intelligence
from scint.intelligence.models import Request
from scint.messaging.models import Message, UserMessage, SystemMessage, Arguments
from scint.support.types import List, Dict, Tuple, Any
from scint.support.logging import log


from abc import ABC, abstractmethod
from enum import Enum, auto
from uuid import uuid4


class Controller(Context):
    def __init__(self):
        super().__init__()
        self.contexts: Dict[str, Context] = {}
        self.location = self.at(region)

    def at(self, region):
        locations = region.locations
        log.info(f"Initialized region with {len(locations)} locations")
        return region

    async def process(self, message: Message):
        log.info(f"Searching for an appropriate context.")
        embedding = message.embedding
        location, similarity = self.location.get_location(embedding)
        if location:
            contexts_at_location = [
                ctx for ctx in self.contexts.values() if ctx.location == location
            ]
            if contexts_at_location:
                for context in contexts_at_location:
                    async for response in context.process(message):
                        yield response
            else:
                log.warning(f"No contexts found at location {location.id}")
        else:
            log.warning("No suitable location found.")

    def get_context(self, context_id: str):
        return self.contexts.get(context_id)

    def get_location(self, context_id: str):
        return self.contexts.get(context_id)

    def add_context(self, context: Context):
        self.contexts[context.id] = context
        context.add_observer(self)
        log.info(f"Added context {context.id} to global context")

    def remove_context(self, context_id: str):
        if context_id in self.contexts:
            context = self.contexts[context_id]
            context.remove_observer(self)
            del self.contexts[context_id]
            log.info(f"Removed context {context_id} from global context")

    async def send_context(self, context: Context, embedding: np.ndarray):
        location, similarity = self.region.get_location(embedding)
        if location:
            await context.at(location, None)
            self.add_context(context)
            log.info(f"Deployed {context.id} to {location.id} with {similarity}.")
        else:
            log.warning(f"No suitable location found for {context.id}.")

    def update(self, context: Context):
        log.info(f"Context {context.id} state changed to {context.state}")
        # Implement any global logic based on context state changes

    async def broadcast_message(self, message: Message, embedding: np.ndarray):
        nearest_locations = self.region.get_nearest_locations(embedding, n=3)
        for location, similarity in nearest_locations:
            contexts_at_location = [
                ctx for ctx in self.contexts.values() if ctx.location == location
            ]
            for context in contexts_at_location:
                async for response in context.process(message):
                    yield response

    def get_active_contexts(self):
        return [ctx for ctx in self.contexts.values() if ctx.state == State.active]

    def get_contexts_by_state(self, state: State):
        return [ctx for ctx in self.contexts.values() if ctx.state == state]

    def get_contexts_by_location(self, location: Location):
        return [ctx for ctx in self.contexts.values() if ctx.location == location]

    def get_region_summary(self):
        total_locations = len(self.region.get_all_locations())
        total_contexts = len(self.contexts)
        active_contexts = len(self.get_active_contexts())
        return {
            "total_locations": total_locations,
            "total_contexts": total_contexts,
            "active_contexts": active_contexts,
        }

    async def update_region(self, new_locations: List[Tuple[Location, np.ndarray]]):
        for location, embedding in new_locations:
            self.region.add_location(location, embedding)
        log.info(f"Updated region with {len(new_locations)} new locations")

    async def cleanup_inactive_contexts(self, max_inactive_time: float):
        current_time = time.time()
        contexts_to_remove = []
        for context_id, context in self.contexts.items():
            if (
                context.state == State.inactive
                and (current_time - context.last_active_time) > max_inactive_time
            ):
                contexts_to_remove.append(context_id)

        for context_id in contexts_to_remove:
            self.remove_context(context_id)

        log.info(f"Cleaned up {len(contexts_to_remove)} inactive contexts")

    async def process_batch(self, messages: List[Tuple[Message, np.ndarray]]):
        results = []
        for message, embedding in messages:
            async for response in self.process(message, embedding):
                results.append(response)
        return results

    def get_context_distribution(self):
        distribution = {}
        for location in self.region.get_all_locations():
            contexts_count = len(self.get_contexts_by_location(location))
            distribution[location.id] = contexts_count
        return distribution


controller = Controller()
