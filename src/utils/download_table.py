import asyncio
import os
import time
from typing import Any
from playwright.async_api import async_playwright, BrowserContext
from tqdm.asyncio import tqdm_asyncio
import aiofiles


async def download_table(context: BrowserContext, file_prefix: str, url: str) -> None:
    """Downloads HTML content from a given URL and saves it to a .txt file."""
    
    page = await context.new_page()

    try:
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        })
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await page.goto(url)

        time.sleep(1)

        await page.wait_for_selector("#ps_search_results", timeout=60000)

        html_content = await page.inner_html("#ps_search_results")
        os.makedirs(os.path.dirname(file_prefix), exist_ok=True)

        async with aiofiles.open(file_prefix, "w", encoding="utf-8") as f:
            await f.write(html_content)

    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
    finally:
        await page.close()


async def download_all_tables(pairs: dict[str, str], max_concurrent_tasks: int = 8) -> None:
    """Orchestrates downloading multiple tables concurrently."""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        context = await browser.new_context()
        semaphore = asyncio.Semaphore(max_concurrent_tasks)

        async def limited_download(file_prefix: str, url: str):
            async with semaphore:
                return await download_table(context, file_prefix, url)

        tasks = [limited_download(file_prefix, url) for file_prefix, url in pairs.items()]
        await tqdm_asyncio.gather(*tasks)

        await context.close()
        await browser.close()