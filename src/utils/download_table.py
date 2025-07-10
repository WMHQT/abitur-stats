import aiofiles
import asyncio
import os
from playwright.async_api import async_playwright, BrowserContext
import time
from tqdm.asyncio import tqdm_asyncio


async def download_table(context: BrowserContext, file_prefix: str, url: str) -> None:
    """Downloads HTML content from a given URL and saves it to a .txt file."""
    page = await context.new_page()

    try:
        await page.goto(url)
        time.sleep(1)
        await page.wait_for_selector("#ps_search_results", timeout=30000)
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
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        semaphore = asyncio.Semaphore(max_concurrent_tasks)

        async def limited_download(file_prefix: str, url: str):
            async with semaphore:
                return await download_table(context, file_prefix, url)

        tasks = [limited_download(file_prefix, url) for file_prefix, url in pairs.items()]
        await tqdm_asyncio.gather(*tasks)

        await context.close()
        await browser.close()