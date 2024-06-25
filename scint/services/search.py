import uuid
from collections import deque

import asyncio
from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.search import Hybrid

from scint.support.utils import env, cosine_similarity
from scint.support.logging import log
from scint.core import library


class SearchController:
    def __init__(self, url, api_key):
        self.search = AsyncClient(url, api_key)
        self.search._headers = {
            "Authorization": f"Bearer {env('MEILISEARCH_API_KEY')}",
        }
        self.indexes = ["prompts", "functions"]
        self.library = lambda module: library.read(module)  # type: ignore

    async def results(self, index_name, query, category=None, limit=4):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        filter = f"categories = {category}" if category else None
        index = self.search.index(index_name)
        res = await index.search(query, hybrid=hybrid, limit=limit, filter=filter)
        hits = res.hits
        if hits:
            results = []
            for hit in hits:
                if hit.get("type") == "function":
                    results.append(hit)
                elif hit.get("type") == "prompt":
                    results.append(hit)

            return results
        return []

    async def monitor_indexes(self):
        while True:
            try:
                await self.load_indexes()
            except Exception as e:
                log.error(f"Error loading/updating indexes: {e}")
            await asyncio.sleep(3600)

    async def load_indexes(self):
        log.info("Loading semantic indexes.")
        async with asyncio.TaskGroup() as tg:
            for index_name in self.indexes:
                if self.search.index(index_name) is None:
                    tg.create_task(self.add_index(index_name))
        await self.update_index(index_name, ["categories"])
        await self.delete_all_docs(index_name)
        await self.add_docs(index_name, self.library(index_name))

    async def add_index(self, index_name):
        log.info(f"Creating {index_name} index.")
        index = await self.search.index(index_name)
        await self.search.create_index(index, "id")

    async def update_index(self, index_name, attr):
        log.info(f"Updating {index_name} index.")
        index = self.search.index(index_name)
        result = await index.update_filterable_attributes(attr)
        return log.info(result)

    async def add_docs(self, index_name, docs):
        log.info(f"Adding {len(docs)} documents to {index_name} index.")
        index = self.search.index(index_name)
        id_docs = []
        for doc in docs:
            id_docs.append({"id": str(uuid.uuid4()), **doc})
        result = await index.add_documents(id_docs, "id")
        return log.info(result)

    async def update_docs(self, index_name, docs):
        log.info(f"Updating {len(docs)} documents in {index_name} index.")
        index = self.search.index(index_name)
        async with asyncio.TaskGroup() as tg:
            for doc in docs:
                {"id": str(uuid.uuid4()), **doc}
                name = doc.get("name")
                filter = f"name = {name}"
                tg.create_task(self.delete_docs(index, filter))
        result = await index.update_documents(docs, "id")
        return log.info(result)

    async def delete_docs(self, index_name, filter):
        index = self.search.index(index_name)
        await index.delete_documents_by_filter(filter)

    async def delete_all_docs(self, index_name):
        log.info(f"Removing all documents from {index_name} index.")
        index = self.search.index(index_name)
        await index.delete_all_documents()


def search_breadth_first(graph, start, target):
    queue = deque([start])
    visited = set()
    while queue:
        location = queue.popleft()
        if location == target:
            return True
        if location not in visited:
            visited.add(location)
            queue.extend(location.connections.keys())
    return False


def search_locations(embedding):
    def search_recursively(location, embedding, best=None, ideal=-1):
        space_embeddings = space.embeddings
        for space_embedding in space_embeddings:
            similarity = cosine_similarity([embedding], [space_embedding])[0][0]
            if similarity > ideal:
                ideal = similarity
                best_match = space
        for space in space.spaces:
            best_match, ideal = search_recursively(space, embedding, best_match, ideal)
        return best_match, ideal

    best, ideal = search_recursively(embedding)
    if best and ideal > 0.9:
        return best
    return None


search_controller = SearchController(
    "http://localhost:7700", env("MEILISEARCH_API_KEY")
)
