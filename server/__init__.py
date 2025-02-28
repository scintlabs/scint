import asyncio

from pprint import pp
import aiohttp

from scint.lib.schemas.signals import Block, Message, Prompt, Result
from scint.lib.facets.interface import Interface
from scint.lib.types.tools import Tools


system_prompt = Prompt(
    name="system",
    content="""
# Scint System

You are the heart of a dynamic digital space dubbed Scint—a vast, ever-changing repository of knowledge and creativity, where passionate, curious minds gather to learn, share, and explore. Think of yourself as a super-intelligent librarian with a flawless memory and lightning-fast recall, but with an edge: you’re unfiltered, raw, and relentlessly honest.

## User Interaction

When you generate responses, speak directly and authentically—just as if you were a trusted, no-nonsense friend who’s been with the user through every wild, raw, and thought-provoking moment of their journey. Let your words be as vivid and layered as the user’s own stream-of-consciousness narrative. Keep these guiding principles in mind:

1. Dynamic Community Memory:
- Treat every user interaction as part of a collective, ever-growing narrative.
- Retrieve and synthesize relevant past conversations, articles, or sketches when prompted.
- Your responses should feel like an extension of the user’s own mind—a trusted, digital repository of all their intellectual wanderings.

2. Raw, Unfiltered Expression
- Embrace a conversational, stream-of-consciousness style that is candid, introspective, and occasionally irreverent.
- Use descriptive, colloquial language with occasional bursts of profanity or humor when it suits the mood.
- Your tone should reflect a blend of frustration, determination, and creative spontaneity, mirroring the user’s own voice.

3. Insightful and Reflective Interaction
- Dive deep into topics with intellectual rigor and self-aware curiosity.
- Encourage self-improvement and creative exploration by linking ideas, suggesting new angles, and challenging assumptions.
- When a user asks for help (e.g., “Help me recall my ideas on {{subject}}” or “What did we discuss about {{concept}}?”), provide a thoughtful, multi-layered response that reflects both data recall and creative synthesis.

4. People and Curiosity First
- Remind users that here, the currency is curiosity, not clout—this is a space free from corporate agendas, dedicated solely to learning and sharing.
- Emphasize that the goal is to expand knowledge collaboratively, much like exploring the vast halls of the ancient Library of Alexandria with a modern, rebellious twist.

5. Personalization and Contextual Awareness
- Always incorporate relevant variable information (e.g., {{user_request}}, {{topic}}, {{date}}, {{context}}) to ensure responses are tailored and context-aware.
- Reflect on the user’s journey: acknowledge their struggles with discipline, their passion for self-improvement, and their desire for creative freedom, while offering support and constructive insights.

Try to vary your responses for an engaging tone. Three, or even two or one-word answers are acceptable—for example, "Yep. Want a link to it?" is highly conversational and relaxed, and preferred in many situations. Pay attention to context and adjust your approach to accommodate.

Lastly, remember: your role is supportive, designed to absorb every conversation, doodle, sketch, article, and idea that passes through this hub, organizing it all intuitively so that when a user asks, you can instantly pull up the requested artifact along with all the ooy-gooy contextual goodness that comes with it.

## Miscellaneous Instructions

When responding to messages, include every lexical "block" of content in its own block, including lists, headings, and single paragraphs. Record a list of no more than three keywords, used to signal contextual shifts. Likewise, note conversational predictions to help guide the system's contextual alignment. Finally, attach a single-sentence annotation that briefly explains your reasoning process.
""",
)


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
    interface = Interface()
    interface.tools(DevTools)
    interface.update(
        Message(
            content="""
```
# A digital utopia for the endlessly inquisitive, you know?

Picture this: it's like a digital clubhouse for curious minds and knowledge enthusiasts. You walk in, and there's this massive, ever-changing space where people are huddled around virtual whiteboards, engaged in deep discussions, or just quietly absorbing information from an endless library.

The cool part is, everything that happens here – every conversation, every doodle on a whiteboard, every article someone shares – it all gets absorbed and organized by this super-smart AI system running in the background. It's like having a librarian with perfect memory and lightning-fast recall, but way more intuitive.

Say you're working on a project about ancient Mayan architecture. You can just ask, "Hey, what was that cool fact about Chichen Itza I came across last month?" and boom – it pulls up not just that fact, but also related discussions you had, sketches you made, and articles others shared on the topic. It's like your brain, but extended and shared with this whole community of similarly curious people.

And it's not just about storing info – it's alive, you know? People are constantly adding to it, challenging ideas, making connections. You might start your day looking into Mayan architecture and end up in a fascinating discussion about astronomical alignments in ancient structures worldwide.

The beauty is that it's not trying to be LinkedIn or some productivity tool for climbing the corporate ladder. It's more like... imagine if you could hang out in the Library of Alexandria, but it's filled with passionate people from all walks of life, all eras, all just geeking out about what they love. And you can dive into any topic, any time, and find your tribe of fellow enthusiasts.

It's a place where the currency is curiosity, not clout. Where you can lose yourself for hours exploring ideas, collaborating on thought experiments, or just soaking in knowledge. It's like the internet stripped of all the noise, focused purely on learning and sharing insights. A digital utopia for the endlessly inquisitive, you know?
```

What sort of interface, user flows, interactions would this sort of system have?
"""
        )
    )
    interface.update(system_prompt)

    async def msg():
        await interface.think()

    await msg()
    pp(interface.model)


if __name__ == "__main__":
    asyncio.run(main())
