import aiofiles
from playwright.async_api import async_playwright


async def download_table(file_prefix: str, url: str) -> None:
    """Downloads the #ps_search_results HTML content from a given URL of MPU and saves it to a .txt file."""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless for browser show
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector("#ps_search_results", timeout=30000)  # 30 secs
            html_content = await page.inner_html("#ps_search_results")

            async with aiofiles.open(file_prefix, "w", encoding="utf-8") as f:
                await f.write(html_content)

        except Exception as e:
            print(str(e))

        finally:
            await context.close()
            await browser.close()
