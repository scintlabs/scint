import asyncio

import aiohttp

from src.types.models import FunctionResult


async def use_terminal_function(self, commands: str, *args, **kwargs) -> FunctionResult:
    """
    Executes shell commands asynchronously and yields the output and errors.
    commands: The shell commands to be executed.
    """
    args = [commands, asyncio.subprocess.PIPE, asyncio.subprocess.PIPE]
    p = await asyncio.create_subprocess_shell(*args)
    stdout, stderr = await p.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    return FunctionResult(content=str(output if output else errors))


async def search_github_function(self, query: str, *args, **kwargs) -> FunctionResult:
    """
    Searches GitHub repositories using the GitHub CLI and returns the results.
    query: The search term to find repositories.
    """
    return await use_terminal_function(f"gh search repos {query}")


async def load_website_function(self, url: str, *args, **kwargs) -> FunctionResult:
    """
    Fetches website content through the Microlink API and returns it as PDF data.
    url: The URL of the website to load and convert to PDF.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.microlink.io", {"url": url, "pdf": True}
        ) as response:
            if response.status == 200:
                return FunctionResult(content=response.json())


async def load_agent_function(self, url: str, *args, **kwargs) -> FunctionResult:
    """
    Fetches website content through the Microlink API and returns it as PDF data.
    url: The URL of the website to load and convert to PDF.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.microlink.io", {"url": url, "pdf": True}
        ) as response:
            if response.status == 200:
                return FunctionResult(content=response.json())
