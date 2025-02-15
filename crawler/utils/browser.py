
def fetch_html_content_by(web_url) -> str:

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        page = browser.new_page()
        page.goto(web_url)
        result = page.content()
        browser.close()
        return result