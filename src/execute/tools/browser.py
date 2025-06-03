from __future__ import annotations

import asyncio
from enum import Enum
from importlib import import_module
import aiohttp
from typing import Literal, TypeAlias

from tavily import AsyncTavilyClient

from src.base.utils import env


Depth: TypeAlias = Literal["basic", "advanced"]
Age: TypeAlias = Literal["day", "week", "month", "year"]


class OutputFormat(Enum):
    Instructions = ("Instructions", None)
    Message = ("Message", None)
    Metadata = ("Metadata", None)
    Notification = ("Notification", None)
    Activity = ("ToolCall", None)
    ToolCall = ("ToolCall", None)

    def __init__(self, format, func):
        self.format = format
        self.func = func

    def __call__(self):
        mod = import_module("src.base.records")
        cls = getattr(mod, self.format)
        return cls


async def search_web(query: str, depth: Depth = "advanced", age: Age = "year"):
    client = AsyncTavilyClient(env("TAVILY_API_KEY"))
    res = await client.search(query=query, search_depth=depth, time_range=age)
    return [r for r in res["results"]]


async def fetch_webpage(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return False, f"Failed with status code: {response.status}"
            content = await response.text()
            return True, content


async def download_file(url: str, save_path: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return False, f"Failed with status code: {response.status}"
            content = await response.read()
            with open(save_path, "wb") as f:
                f.write(content)
            return True, f"File downloaded to {save_path}"


async def post_request(url: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            status = response.status
            response_text = await response.text()
            try:
                response_json = await response.json()
                return status == 200, response_json
            except Exception:
                return status == 200, response_text


async def use_terminal(command: str):
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    if errors:
        return process.returncode == 0, {"output": output, "errors": errors}
    return True, output


async def task_handoff(target_activity, custom_prompt, context):
    valid_activities = [
        "composition",
        "dialogue",
        "execution",
        "prediction",
        "reasoning",
    ]
    if target_activity.lower() not in valid_activities:
        raise ValueError(f"Activity must be one of: {', '.join(valid_activities)}")

    return


async def complete_task(results: str):
    pass
