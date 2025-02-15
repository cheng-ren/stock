import time

from configs.path_config import DEFAULT_CHROME_DRIVER_PATH


# def fetch_html_content_by(web_url) -> str:
#
#     from playwright.sync_api import sync_playwright
#
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
#         page = browser.new_page()
#         page.goto(web_url)
#         result = page.content()
#         browser.close()
#         return result


def fetch_html_content_by(web_url) -> str:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service

    service = Service(DEFAULT_CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 启动无头模式
    driver = webdriver.Chrome(options, service)

    driver.get(web_url)
    source = driver.page_source
    driver.quit()
    return source


if __name__ == '__main__':
    a = fetch_html_content_by('https://guba.eastmoney.com/list,600120,1,f.html')
    print(a)