import asyncio

from pprint import pp
import aiohttp

from scint.lib.actors.interface import Interface
from scint.lib.compose import Composer
from scint.lib.exchange import Exchange
from scint.lib.schema.context import ActiveState, SemanticState
from scint.lib.types.prompts import Content
from scint.lib.schema.signals import Result
from scint.lib.types.tools import Tools


exchange = Exchange()
composer = Composer()


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
                        return Content(content=image)
                else:
                    return Content(content="Failed to download image.")

    async def load_website(self, url: str, *args, **kwargs):
        """
        Fetches website content through the Microlink API and returns it as PDF data.
        url: The URL of the website to load and convert to PDF.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.microlink.io",
                {"url": url, "pdf": True},
            ) as response:
                if response.status == 200:
                    return Content(content=response.json())


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
        return Result(content=Content(content=str(output if output else str(errors))))

    async def search_github(self, query: str, *args, **kwargs):
        """
        Searches GitHub repositories using the GitHub CLI and returns the results.
        query: The search term to find repositories.
        """
        process = await asyncio.create_subprocess_shell(
            f"gh search repos {query}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() if stdout else ""
        errors = stderr.decode().strip() if stderr else ""
        return Content(content=errors) if errors else Content(content=output)


class Context(Interface):
    """
    Context Interface
    This class provides methods to access and manage different states of context in a conversational AI system. When messages arrive, choose the most appropriate state given the message.
    """

    _active: ActiveState = ActiveState()
    _semantic: SemanticState = SemanticState()

    async def active_state(self, mixed: bool):
        """
        This function selects the system's activate state, showing the latest interactions and focused information between the user and the system.
        mixed: Setting this to false provides total focus on the active state.
        """

        messages = [self._active.goal, *self._active.events, *self._active.messages]

        if mixed:
            pp("Getting mixed active state.")
            return {"messages": messages, "tools": self._active.tools}
        pp("Getting full active state.")
        return {"messages": messages, "tools": self._active.tools}

    async def semantic_state(self, mixed: bool):
        """
        This function accesses the system's semantic state, providing a broader context and deeper understanding of the ongoing conversation.
        mixed: Setting this to false provides pure semantic data.
        """

        messages = [self._active.goal, *self._active.events, *self._active.messages]

        if mixed:
            pp("Getting mixed semantic state.")
            return {"messages": messages, "tools": self._active.tools}
        pp("Getting full semantic state.")
        return {"messages": messages, "tools": self._active.tools}


async def main():
    context = Context()
    res = await context.process()
    pp(context.model)
    pp(res)

    # async def first():
    #     message = Message(content="What functions do you have access to currently?")
    # interface.update(message)
    # res = await interface.process()
    # if res:
    #     print(interface.context.messages[-1].model_dump())

    # return await second()

    # async def second():
    #     message = Message(content="Great. And how about now?")
    #     interpreter.context.update(message)
    #     res = await interpreter.process()
    #     if res:
    #         print(interpreter.context.messages[-1].content)

    # await first()


if __name__ == "__main__":
    asyncio.run(main())
