from typing import Dict

from services.logger import log


async def create_content(content_type: str, content: str) -> Dict[str, str]:
    log.info("Worker: creating content.")

    return {
        "role": "system",
        "content": f"{content_type}: {content}",
        "name": "create_content",
    }
