import asyncio

from pprint import pp
import aiohttp


from scint.lib.prototypes.interface import Interface
from scint.lib.prototypes.composer import Composer
from scint.lib.schemas.context import InterfaceContext, ComposedContext
from scint.lib.schemas.signals import Message, Result
from scint.lib.types.tools import Tools


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
                "https://api.microlink.io",
                {"url": url, "pdf": True},
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
        return Result(content=Message(content=str(output if output else str(errors))))

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
        return Message(content=errors) if errors else Message(content=output)


class Context(Interface):
    """
    Context Interface
    This class provides methods to access and manage different states of context in a conversational AI system. When messages arrive, choose the most appropriate state given the message.
    """

    _active: InterfaceContext = InterfaceContext()
    _semantic: ComposedContext = ComposedContext()

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
