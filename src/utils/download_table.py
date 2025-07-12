import asyncio
import os
import random
import time
from typing import Any
from playwright.async_api import async_playwright, BrowserContext
from tqdm.asyncio import tqdm_asyncio
import aiofiles


async def download_table(context: BrowserContext, file_prefix: str, url: str) -> None:
    """Downloads HTML content from a given URL and saves it to a .txt file."""
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ]

    page = await context.new_page()
    attempt = 0

    while attempt < 5:  # Try up to 5 times with different user agents
        try:
            user_agent = random.choice(user_agents)
            await page.set_extra_http_headers({"User-Agent": user_agent})
            await page.set_viewport_size({"width": 1920, "height": 1080})
            await page.goto(url)

            time.sleep(1)

            await page.wait_for_selector("#ps_search_results", timeout=60000)

            html_content = await page.inner_html("#ps_search_results")
            os.makedirs(os.path.dirname(file_prefix), exist_ok=True)

            async with aiofiles.open(file_prefix, "w", encoding="utf-8") as f:
                await f.write(html_content)

            break  # Exit the loop if successful

        except Exception as e:
            print(f"Error downloading {url} with user agent '{user_agent}': {str(e)}")
            attempt += 1
            if attempt < 5:
                print("Retrying with a different user agent...")

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