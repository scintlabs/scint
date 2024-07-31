# from enum import Enum, auto
# from datetime import datetime
# from abc import ABC, abstractmethod
# from typing import Dict, Optional

# import numpy as np
# from pydantic import Field

# from scint.orchestration.journal import log


# class Distrubitor(BaseContext):
#     def __init__(self):
#         super().__init__()

#     async def _extract_context(self, context):
#         log.info(f"Extracting context.")
#         content = []
#         for message in context.get("messages"):
#             for String in message.content:
#                 content.append(String.get("data"))
#         return "\n".join(content)

#     async def coordinate(self, context: Context):
#         log.info(f"Preparing context parameters.")
#         query = await self._extract_context(context)
#         prompt_args = ["identities", "instructions"]
#         func_args = ["interact"]
#         prompts = await self._get_prompts(query, prompt_args, "prompts")
#         functions = await self._get_functions(query, func_args, "functions")
#         return prompts, functions

#     async def coordinate(self, message: Message):
#         log.info(f"Searching for context.")
#         try:
#             log.info(message.header.context)
#             if message.header.context is not None:
#                 prev_context = self.get_context(message.header.context)
#                 if prev_context is not None:
#                     async for res in self.send_message(prev_context, message):
#                         yield res
#             else:
#                 location = await self.get_location(message.embedding)
#                 next_context = await self.create_context(location)
#                 response = self.send_message(next_context, message)
#                 async for res in response:
#                     yield res
#         except Exception as e:
#             log.info(e)

#     async def get_location(self, embedding):
#         return await self.location.get_matching_location(embedding)

#     async def get_context(self, id: int):
#         for key, value in self.contexts.items():
#             if key == id:
#                 return value
#             return None

#     async def create_context(self, location: Location):
#         log.info(f"Creating new context.")
#         context = Context(location)
#         self.contexts[context.id] = context.id
#         return context

#     async def send_message(self, context: Context, message: Message):
#         async for res in context.process(message):
#             yield res

#     async def broadcast_message(self, message: Message, embedding: np.ndarray):
#         nearest_locations = self.location.get_nearest_locations(embedding, n=3)
#         for location, similarity in nearest_locations:
#             contexts_at_location = [
#                 ctx for ctx in self.contexts.values() if ctx.location == location
#             ]
#             for context in contexts_at_location:
#                 async for response in context.process(message):
#                     yield response

#     # def get_active_contexts(self):
#     #     return [ctx for ctx in self.contexts.values() if ctx.state == State.active]

#     # def get_contexts_by_location(self, location: Location):
#     #     return [ctx for ctx in self.contexts.values() if ctx.location == location]

#     # async def cleanup_inactive_contexts(self, max_inactive_time: float):
#     #     current_time = time.time()
#     #     contexts_to_remove = []
#     #     for context_id, context in self.contexts.items():
#     #         if (
#     #             context.state == State.inactive
#     #             and (current_time - context.last_active_time) > max_inactive_time
#     #         ):
#     #             contexts_to_remove.append(context_id)

#     #     for context_id in contexts_to_remove:
#     #         self.remove_context(context_id)

#     #     log.info(f"Cleaned up {len(contexts_to_remove)} inactive contexts")

#     # async def process_batch(self, messages: List[Tuple[Message, np.ndarray]]):
#     #     results = []
#     #     for message, embedding in messages:
#     #         async for response in self.process(message, embedding):
#     #             results.append(response)
#     #     return results

#     # def get_context_distribution(self):
#     #     distribution = {}
#     #     for location in self.region.get_all_locations():
#     #         contexts_count = len(self.get_contexts_by_location(location))
#     #         distribution[location.id] = contexts_count
#     #     return distribution


# coordinator = Distrubitor(Region())
