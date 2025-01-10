from meilisearch_python_sdk.models.search import Hybrid
from meilisearch_python_sdk import AsyncClient

from src.core.types import Aspect
from ..util.utils import env


class Finder(Aspect):
    client = AsyncClient(env("MEILISEARCH_URL"), env("MEILISEARCH_API_KEY"))

    async def search(self, index_name, query, category=None, limit=4):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        category_filter = f"categories = {category}" if category else None
        index = self.client.index(index_name)
        res = await index.search(
            query, hybrid=hybrid, limit=limit, filter=category_filter
        )
        return res.hits
