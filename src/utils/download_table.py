from playwright.sync_api import sync_playwright


def download_table(url: str, name: str):
    ''' Downloads dynamicly generated table from site. '''

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # headless for browser show
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        print("Page loaded. Waiting for <div id=\"ps_search_results\" style=\"...\">")
        
        try:
            page.wait_for_selector("#ps_search_results", timeout=10000) # 10 secs
            html_content = page.inner_html("#ps_search_results")

            with open("f{}.txt", "w", encoding="utf-8") as f:
                f.write(html_content)

            print("Saved div content to f{}.txt")

        except Exception as e:
            print("Error:", str(e))
            print("Saving full page HTML for debugging...")
            with open("full_page.html", "w", encoding="utf-8") as f:
                f.write(page.content())

        finally:
            context.close()
            browser.close()