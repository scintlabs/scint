import aiohttp

from discord import Client, Intents
from app.services.logging import logger
from app.system.config import envar


intents = Intents.default()
intents.message_content = True
discord_token = envar("DISCORD_TOKEN")
endpoint = "http://localhost:8000/chat"


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
                    await message.channel.send(reply)

                except Exception as e:
                    logger.exception(f"Error: {e}")
                    await message.channel.send(
                        "An error occurred while processing your request."
                    )
                return


Client = ScintDiscordClient(intents=intents)
Client.run(discord_token)  # type: ignore
