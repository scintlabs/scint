import aiohttp
import asyncio


async def check_meilisearch():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("http://localhost:7700/health") as response:
                print(f"Meilisearch health check status: {response.status}")
                print(await response.text())
        except aiohttp.ClientError as e:
            print(f"Failed to connect to Meilisearch: {e}")


asyncio.run(check_meilisearch())
