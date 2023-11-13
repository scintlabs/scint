import json
import re

import aiohttp
from discord import Client, Intents

from core.config import API_CHAT_ENDPOINT, DISCORD_SCINT_TOKEN
from core.util import split_discord_message
from services.logger import log

intents = Intents.default()
intents.message_content = True


async def chat_request(content, author):
    request = {"message": {"role": "user", "content": content, "name": author}}

    async with aiohttp.ClientSession() as session:
        async with session.post(API_CHAT_ENDPOINT, json=request) as res:
            if res.status != 200:
                log.info(await res.text())
                return

            while True:
                response_line = await res.content.readline()

                if not response_line:
                    break

                response = json.loads(response_line.decode("utf-8"))

                if response:
                    yield response.get("content")

                else:
                    log.error("Response does not contain a content key.")


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
                    async for reply in chat_request(content, author):
                        log.info(f"API Reply: {reply}")
                        for chunk in split_discord_message(reply):
                            await message.channel.send(chunk)

                except Exception as e:
                    log.exception(f"Error: {e}")
                    await message.channel.send(
                        "An error occurred while processing your request."
                    )
                return


scint_discord = ScintDiscordClient(intents=intents)
scint_discord.run(DISCORD_SCINT_TOKEN)
