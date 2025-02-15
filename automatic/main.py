import re

from crawler.utils.browser import fetch_html_content_by
from crawler.utils.dongfangcaifu import fetch_news_from_dfcf
from lxml import etree
from database_stock.exec import sync_stock

if __name__ == '__main__':
    # count, items = fetch_news_from_dfcf(stock_code=600120, fetch_end_time='2025-02-13 00:00:00')
    # print(count)
    # print(items)


    html_content = fetch_html_content_by("https://quote.eastmoney.com/stocklist.Html")
    root = etree.HTML(html_content)
    nodes = root.xpath('//div[@class="qox"]//li/a')
    # print(html_content)
    print(len(nodes))
    for item in nodes:
        if item.text is not None:
            match = re.search(r'([^\(]+)\((\d+)\)', item.text)
            if match:
                name = match.group(1).strip()  # 股票名称
                code = match.group(2)  # 股票代码
                sync_stock({"code":code, "title": name})
            else:
                print("No match found")