from playwright.sync_api import sync_playwright

url = "https://mospolytech.ru/postupayushchim/priem-v-universitet/rating-abiturientov/?qs=MDAwMDAwMDU2XzAxfDIzLjAzLjAyX9CT0L7QvdC%2B0YfQvdGL0LUg0LDQstGC0L7QvNC%2B0LHQuNC70Lgg0Lgg0LzQvtGC0L7RhtC40LrQu9GLfNCe0YfQvdCw0Y980JHRjtC00LbQtdGC0L3QsNGPINC%2B0YHQvdC%2B0LLQsA%3D%3D"  # Replace with actual URL

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Show browser window
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)

    print("🌐 Page loaded. Waiting for div#ps_search_results...")
    
    try:
        # Wait for div to appear
        page.wait_for_selector("#ps_search_results", timeout=30000)
        html_content = page.inner_html("#ps_search_results")

        # Save to file
        with open("ps_search_results.txt", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("✅ Saved div content to ps_search_results.txt")

    except Exception as e:
        print("❌ Error:", str(e))
        print("📄 Saving full page HTML for debugging...")
        with open("full_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

    finally:
        input("Press Enter to close browser...")
        context.close()
        browser.close()