from typing import Any, List


class MaterializedViewQuery:
    def __init__(self, view_store):
        self.view_store = view_store

    async def get_documents_by_label(self, label: str) -> List[Any]:
        docs = await self.view_store.query()
        return [doc for doc in docs if label in doc.labels]

    async def get_documents_by_sentiment_range(self, min: float, max: float):
        docs = await self.view_store.query()
        return [
            doc
            for doc in docs
            if doc.sentiment_score and min <= doc.sentiment_score <= max
        ]

    async def get_failed_documents(self):
        return await self.view_store.query()
