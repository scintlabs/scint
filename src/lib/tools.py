from __future__ import annotations

import asyncio
import aiohttp
import base64
from typing import Literal, TypeAlias

from PIL import Image
from io import BytesIO
from tavily import AsyncTavilyClient

from src.core.util.constants import env


Depth: TypeAlias = Literal["basic", "advanced"]
Age: TypeAlias = Literal["day", "week", "month", "year"]


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


async def download_image(url: str, resize=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return False, f"Failed with status code: {response.status}"

            content = await response.read()

    img = Image.open(BytesIO(content))
    if resize:
        width, height = resize
        img = img.resize((width, height))

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    return True, base64_image


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


async def main():
    await search_web("lang graph github")
