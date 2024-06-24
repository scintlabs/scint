import asyncio
import aiohttp

from scint.core.containers.blocks import SystemMessage
from scint.support.utils import encode_image


def with_metadata():
    def decorator(func):
        func.metadata = func.__name__
        return func

    return decorator


async def download_image(image_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                with open("download.png", "wb") as f:
                    image = await response.read()
                    base64_image = encode_image(image)
                    yield SystemMessage(f"data:image/;base64,{base64_image}")
            else:
                yield SystemMessage(content="Failed to download image.")


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
