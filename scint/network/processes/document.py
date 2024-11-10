from typing import Dict, List

from scint.repository.models.collections import Document
from scint.repository.models.states import ProcessingState


class DocumentProcessor:
    def __init__(self, view):
        self.view = view

    async def process_document(self, doc_id: str, content: str):
        vectors = await self.generate_vectors(content)
        labels = await self.classify(content)
        self.view.update(doc_id, vectors=vectors, labels=labels)

    async def generate_vectors(self, content):
        pass

    async def classify(self, content):
        pass


class EmbeddingStage:
    async def process(self, data: dict) -> dict:
        embeddings = await self.generate_embeddings(data["text"])
        return {**data, "embeddings": embeddings}

    async def generate_embeddings(self, param):
        pass

    async def generate_embeddings(self, param):
        pass


class LabelingStage:
    async def process(self, data: dict) -> dict:
        labels = await self.generate_labels(data["text"])
        return {**data, "labels": labels}

    async def generate_labels(self, param):
        pass


class Pipeline:
    def __init__(self, stages: List[PipelineStage]):
        self.stages = stages

    async def process(self, initial_data: dict) -> dict:
        result = initial_data
        for stage in self.stages:
            result = await stage.process(result)
        return result


class MaterializedViewStore:
    async def update(self, id, processing_state):
        pass


class DocProcessor:
    def __init__(self, view_store: MaterializedViewStore):
        self.view_store = view_store

    async def process_document(self, document: Document):
        await self.view_store.update(
            document.id,
            processing_state=ProcessingState.PROCESSING,
        )

        try:
            embeddings = await self._generate_embeddings(document.content)
            await self.view_store.update(document.id, embeddings=embeddings)

            labels = await self._generate_labels(document.content)
            await self.view_store.update(document.id, labels=labels)

            sentiment = await self._analyze_sentiment(document.content)
            await self.view_store.update(document.id, sentiment_score=sentiment)

            entities = await self._extract_entities(document.content)
            await self.view_store.update(document.id, named_entities=entities)

            await self.view_store.update(
                document.id, processing_state=ProcessingState.COMPLETED
            )

        except Exception as e:
            await self.view_store.update(
                document.id,
                processing_state=ProcessingState.FAILED,
            )

    async def _generate_embeddings(self, content: str) -> List[float]:
        return [0.1, 0.2, 0.3]

    async def _generate_labels(self, content: str) -> List[str]:
        return ["label1", "label2"]

    async def _analyze_sentiment(self, content: str) -> float:
        return 0.8

    async def _extract_entities(self, content: str) -> Dict[str, List[str]]:
        return {"PERSON": ["John Doe"], "ORG": ["Google"]}
