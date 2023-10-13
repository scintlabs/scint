import aiohttp

from discord import Client, Intents
from scint.services.logging import logger
from scint.system.config import envar


intents = Intents.default()
intents.message_content = True
discord_token = envar("DISCORD_TOKEN")
endpoint = "http://localhost:8000/message"


def split_message(message, max_length=2000):
    """
    Splits a message into chunks of max_length. Tries to split by line,
    then by word, then by character if necessary.
    """
    if len(message) <= max_length:
        return [message]

    lines = message.split("\n")
    chunks = []

    current_chunk = ""

    for line in lines:
        # If the line itself is too long, split it by word
        if len(line) > max_length:
            words = line.split(" ")
            for word in words:
                # If the word itself is too long, just add it and start a new chunk
                if len(word) > max_length:
                    if current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = ""
                    chunks.append(word)
                # If adding the word would make the chunk too long, start a new one
                elif len(current_chunk) + len(word) > max_length:
                    chunks.append(current_chunk)
                    current_chunk = word
                else:
                    current_chunk = f"{current_chunk} {word}" if current_chunk else word
        # If adding the line would make the chunk too long, start a new one
        elif len(current_chunk) + len(line) > max_length:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk = f"{current_chunk}\n{line}" if current_chunk else line

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


async def chat_request(content, author, target):
    message = {
        "worker": target,
        "message": {"role": "user", "content": content, "name": author},
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json=message) as res:
            if res.status != 200:
                logger.info(await res.text())

            return await res.json()


class ScintDiscordClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        prefix = "!shard"

        if message.author == self.user:
            return

        if self.user in message.mentions and message.mention_everyone is False:
            async with message.channel.typing():
                try:
                    author = "discord_" + str(message.author)
                    content = message.content.replace(f"<@!{self.user}>", "").strip()
                    reply = await chat_request(content, author, target="scint")
                    logger.info(f"API Reply: {reply}")

                    # Split message into chunks and send each one
                    for chunk in split_message(reply):
                        await message.channel.send(chunk)

                except Exception as e:
                    logger.exception(f"Error: {e}")
                    await message.channel.send(
                        "An error occurred while processing your request."
                    )
                return


Client = ScintDiscordClient(intents=intents)
Client.run(discord_token)  # type: ignore
