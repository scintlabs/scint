from typing import Protocol

from scint.ensemble.components.enum import EnumType


class PipelineStage(Protocol):
    async def process(self, data: dict) -> dict:
        pass


class ProcessingState(EnumType):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
