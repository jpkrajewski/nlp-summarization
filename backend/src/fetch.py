from typing import List, Tuple
import aiohttp
import asyncio
from pydantic import HttpUrl


async def fetch_content(session: aiohttp.ClientSession, url: str) -> Tuple[str, bytes]:
    async with session.get(url) as response:
        content = await response.content.read()
        return url, content


async def fetch_data(urls: List[HttpUrl]) -> list:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_content(session, str(url)) for url in urls]
        return await asyncio.gather(*tasks)
