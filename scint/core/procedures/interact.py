import asyncio
import datetime
import os
import uuid

import aiohttp

from scint.support.logging import log
from scint.messaging import SystemMessage
from scint.support.types import Any
from scint.core import Context


async def search_github_repos(query: str):
    process = await asyncio.create_subprocess_shell(
        f"gh search repos {query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    full_output = output + "\n" + errors if errors else output
    yield SystemMessage(content=f"{full_output}")
