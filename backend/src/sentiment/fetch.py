from typing import List, Tuple
import aiohttp
import asyncio
from pydantic import HttpUrl
import logging
from time import time
from fastapi import logger
from sentiment.profilers import async_profiler


async def fetch_content(session: aiohttp.ClientSession, url: str) -> Tuple[str, bytes]:
    async with session.get(url) as response:
        content = await response.content.read()
        return url, content


@async_profiler
async def fetch_data(urls: List[HttpUrl]) -> list:
    start = time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_content(session, str(url)) for url in urls]
        result = await asyncio.gather(*tasks)
    logger.logger.info(f"Fetching {len(urls)} took: {start - time()}")
    return result
