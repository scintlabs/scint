import httpx
import asyncio
import json
import aiohttp

from discord import Client, Intents
from base.system.logging import logger
from base.system.settings import envar


intents = Intents.default()
intents.message_content = True

endpoint = "http://localhost:8000/chat"
discord_token = envar("DISCORD_TOKEN")


async def chat_request(content, author, target):
    message = {
        "agent": target,
        "message": {"role": "user", "content": content, "name": author},
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json=message) as res:
            if res.status != 200:
                logger.info(await res.text())
            return await res.json()


async def shard_request(content, author, target):
    message = {
        "agent": target,
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

        if message.content.startswith(prefix):
            async with message.channel.typing():
                try:
                    author = "discord_" + str(message.author)
                    content = message.content[len(prefix) :].strip()
                    reply = await chat_request(content, author, target="scint")
                    logger.info(f"API Reply: {reply}")
                    await message.channel.send(reply)

                except Exception as e:
                    logger.exception(f"Error: {e}")
                    await message.channel.send(
                        "An error occurred while processing your request."
                    )

        if self.user in message.mentions and message.mention_everyone is False:
            async with message.channel.typing():
                try:
                    author = "discord_" + str(message.author)
                    content = message.content.replace(f"<@!{self.user}>", "").strip()
                    reply = await shard_request(content, author, target="shard")
                    logger.info(f"API Reply: {reply}")
                    await message.channel.send(reply)

                except Exception as e:
                    logger.exception(f"Error: {e}")
                    await message.channel.send(
                        "An error occurred while processing your request."
                    )
                return


Client = ScintDiscordClient(intents=intents)
Client.run(discord_token)
