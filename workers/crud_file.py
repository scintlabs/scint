from typing import Dict

from services.logger import log


async def crud_file(filepath: str, operation: str, content: str) -> Dict[str, str]:
    log.info("Running Google search query.")

    return {
        "role": "system",
        "content": f"Ran {operation} operation on {filepath} with:\n {content}",
        "name": "create_content",
    }
