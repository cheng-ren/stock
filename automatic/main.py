import re

from crawler.utils.browser import fetch_html_content_by
from crawler.utils.dongfangcaifu import fetch_news_from_dfcf, fetch_stocks_from_dfcf
from lxml import etree
from database_stock.exec import sync_stock

if __name__ == '__main__':
    # count, items = fetch_news_from_dfcf(stock_code=600120, fetch_end_time='2025-02-13 00:00:00')
    # print(count)
    # print(items)

    items = fetch_stocks_from_dfcf()
    for item in items:
        sync_stock(item)