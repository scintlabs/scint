import asyncio
import functools
import os

from kagiapi import KagiClient

from scint.objects.utils import function_metadata
from scint.support.types import SystemMessage
from scint.support.logging import log
from scint.support.utils import envar


async def search_web(query: str):
    search_web.metadata = function_metadata("search_web")
    kagi = KagiClient(envar("KAGI_API_KEY"))
    results = kagi.enrich(query=query)
    for result in results["data"]:
        yield SystemMessage(content=f"{result}")


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
    yield SystemMessage(content=full_output)


async def recursive_getattr(obj, attr, *args):
    async def _getattr(obj, attr):
        try:
            if isinstance(obj, dict):
                return obj[attr]
            elif isinstance(obj, list):
                return obj[int(attr)]
            else:
                return getattr(obj, attr, *args)
        except (KeyError, IndexError, AttributeError):
            return None

    return functools.reduce(_getattr, [obj] + attr.split("."))


async def load_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            yield SystemMessage(content=f"{content}")

    except (UnicodeDecodeError, FileNotFoundError, PermissionError):
        yield None


async def create_directory_map(path):
    dmap = {
        "directory": os.path.basename(path) if os.path.basename(path) else path,
        "data": {
            "directories": [],
            "files": [],
        },
    }

    for i in os.scandir(path):
        if i.is_dir(follow_symlinks=False):
            if i.name in {".git", "__pycache__", ".DS_Store"}:
                continue
            dmap["data"]["directories"].append(create_directory_map(i.path))

        elif i.is_file():
            if i.name.endswith((".txt", ".md", ".py", ".json", ".xml")):
                content = load_file(i.path)
                if content is not None:
                    dmap["data"]["files"].append({"name": i.name, "content": content})

    yield SystemMessage(content=f"{dmap}")


async def use_terminal(commands: str):
    process = await asyncio.create_subprocess_shell(
        commands,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    full_output = output + "\n" + errors if errors else output
    yield SystemMessage(content=full_output)


async def generate_plan():
    pass
