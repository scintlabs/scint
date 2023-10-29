from typing import Dict, List

from services.logger import log


class Context:
    def __init__(self):
        log.info(f"Creating Context.")

        self.context: List[Dict[str, str]] = []

    async def summarize_context(self) -> List[Dict[str, str]]:
        log.info(f"Summarizing Context.")
