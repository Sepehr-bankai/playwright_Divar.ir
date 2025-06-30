import asyncio
from playwright.async_api import async_playwright


#made for blocking images so browser load faster.
async def image_blocker(route, request):
    if request.resource_type == "image":
        await route.abort()
    else:
        await route.continue_()