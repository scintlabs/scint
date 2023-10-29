import aiohttp
import re
from discord import Client, Intents

from services.logger import log
from core.config import DISCORD_SCINT_TOKEN, API_CHAT_ENDPOINT
from core.util import split_discord_message

intents = Intents.default()
intents.message_content = True


async def chat_request(content, author):
    request = {
        "role": "user",
        "content": content,
        "name": author,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_CHAT_ENDPOINT, json=request) as res:
            if res.status != 200:
                log.info(await res.text())

            response = await res.json()
            response_message = response.get("message")
            message_content = response_message.get("content")
            return message_content


class ScintDiscordClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if self.user in message.mentions and message.mention_everyone is False:
            async with message.channel.typing():
                try:
                    author = str(message.author)
                    content = re.sub(r"<@!?[0-9]+>", "", message.content).strip()
                    reply = await chat_request(content, author)
                    log.info(f"API Reply: {reply}")

                    for chunk in split_discord_message(reply):
                        await message.channel.send(chunk)

                except Exception as e:
                    log.exception(f"Error: {e}")
                    await message.channel.send(
                        "An error occurred while processing your request."
                    )
                return


Client = ScintDiscordClient(intents=intents)
Client.run(DISCORD_SCINT_TOKEN)  # type: ignore
