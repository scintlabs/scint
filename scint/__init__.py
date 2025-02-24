import asyncio

from pprint import pp
import aiohttp

from scint.lib.schemas.signals import Block, Message, Result
from scint.lib.prototypes.interface import Interface
from scint.lib.types.tools import Tools


class Loaders(Tools):
    async def load_image(self, url: str, *args, **kwargs):
        """
        Downloads an image from a given URL and saves it locally.
        url: The URL of the image to download.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open("download.png", "wb") as f:
                        image = await f.read()
                        return Message(content=image)
                else:
                    return Message(content="Failed to download image.")

    async def load_website(self, url: str, *args, **kwargs):
        """
        Fetches website content through the Microlink API and returns it as PDF data.
        url: The URL of the website to load and convert to PDF.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.microlink.io", {"url": url, "pdf": True}
            ) as response:
                if response.status == 200:
                    return Message(content=response.json())


class DevTools(Tools):
    async def use_terminal(self, commands: str, *args, **kwargs):
        """
        Executes shell commands asynchronously and yields the output and errors.
        commands: The shell commands to be executed.
        """
        process = await asyncio.create_subprocess_shell(
            commands,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() if stdout else ""
        errors = stderr.decode().strip() if stderr else ""
        return Result(blocks=[Block(content=str(output if output else str(errors)))])

    async def search_github(self, query: str, *args, **kwargs):
        """
        Searches GitHub repositories using the GitHub CLI and returns the results.
        query: The search term to find repositories.
        """
        return await self.use_terminal(f"gh search repos {query}")


async def main():
    ptype = Interface()
    ptype.tools(DevTools)
    ptype.update(
        Message(
            content="Pardon the repeated messages, busy working on your persistent memory."
        )
    )
    print(ptype.context.model)

    async def msg():
        await ptype.think()

    await msg()
    pp(ptype.model)


if __name__ == "__main__":
    asyncio.run(main())
