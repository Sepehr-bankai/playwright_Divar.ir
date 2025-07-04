import asyncio 
from playwright.async_api import async_playwright
from .functions.image_blocker import image_blocker
from .functions.gather_links import gather_links
from .functions.gather_info import gather_info

async def main():
    all_links = await gather_links()
    print("done")
    await gather_info(all_links)

asyncio.run(main())
