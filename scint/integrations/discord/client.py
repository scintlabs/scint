import asyncio
import json
import re

import aiohttp
from discord import Client, Intents

from scint.modules.logging import log

intents = Intents.default()
intents.message_content = True


class ScintDiscord(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.websocket_url = "ws://localhost:8000/ws"
        self.messages = []
        self.last_message_id = None

    async def on_ready(self):
        log.info(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author != self.user:
            if "scint" in message.content or self.user in message.mentions:
                await self.process_message(message)

    async def process_message(self, message):
        if message.id == self.last_message_id:
            return
        self.last_message_id = message.id
        channel = message.channel
        sender = "Main"
        receiver_full = str(self.user)
        receiver = receiver_full.split("#")[0]
        content = re.sub(r"<@!?[0-9]+>", "", message.content).strip()
        if self.messages:
            content = "\n".join(self.messages) + "\n" + content

        try:
            await self.send_to_websocket(
                channel,
                {"sender": sender, "receiver": receiver, "content": content},
            )
        except Exception as e:
            await message.channel.send(f"There were problems: {e}")

    async def send_to_websocket(self, channel, message):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.websocket_url) as ws:
                await ws.send_str(json.dumps(message))
                async for msg in ws:
                    response = json.loads(msg.data)
                    await self.send_message(channel, response)

    async def send_message(self, channel, response):
        await channel.send(response.get("content"))


scint_discord = ScintDiscord(intents=intents)
