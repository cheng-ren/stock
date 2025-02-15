import json
import re
from datetime import datetime, timedelta
from lxml import etree
from crawler.utils.browser import fetch_html_content_by
from utils.log.yc_logger import logger


def fetch_stocks_from_dfcf() -> list:
    html_content = fetch_html_content_by("https://quote.eastmoney.com/stocklist.Html")
    root = etree.HTML(html_content)
    nodes = root.xpath('//div[@class="qox"]//li/a')
    result = []
    for item in nodes:
        if item.text is not None:
            match = re.search(r'([^\(]+)\((\d+)\)', item.text)
            if match:
                name = match.group(1).strip()  # 股票名称
                code = match.group(2)  # 股票代码
                result.append({"code": code, "title": name})
            else:
                print("No match found")
    return result


def fetch_news_from_dfcf(stock_code, fetch_end_time=None, page=1) -> ():
    """
    东方财富网提取资讯
    :param stock_code: 股票代码
    :param fetch_end_time: 索引截止时间, 如果不传入, 则全部提取
    :param page: 索引页码 - 用作根据时间递归查找, 外部无需传入
    :return: 数据个数, 数组
    """
    # 提前转换,以尽早知道参数是否合规
    if fetch_end_time is not None:
        fetch_end_time_date = datetime.strptime(fetch_end_time, "%Y-%m-%d %H:%M:%S")
    else:
        now = datetime.now()
        yesterday = now - timedelta(days=2)
        yesterday_midnight = datetime(yesterday.year, yesterday.month, yesterday.day)
        fetch_end_time_date = yesterday_midnight

    page_param = (("_" if page > 1 else "") + str(page)) if page > 1 else ""
    web_url = f"https://guba.eastmoney.com/list,{stock_code},1,f{page_param}.html"
    html_content = fetch_html_content_by(web_url)
    count_per_page = 80
    match = re.search(r'<script>var article_list=({.*?});</script>', html_content, re.DOTALL)
    if match:
        json_str = match.group(1)
        json_data = json.loads(json_str)
        count = json_data['count']
        items = json_data['re']

        result_items = []
        for item in items:
            post_publish_time_str = item['post_publish_time']
            post_publish_time = datetime.strptime(post_publish_time_str, "%Y-%m-%d %H:%M:%S")
            if fetch_end_time_date <= post_publish_time:  # 符合要求的item
                result_items.append(item)
        if len(result_items) == len(items) and count_per_page * page <= count:  # 全部匹配, 则向下一页查找
            next_count, next_items = fetch_news_from_dfcf(stock_code, fetch_end_time, page + 1)
            r_item = next_items + result_items
            return len(r_item), r_item
        return len(result_items), result_items
    else:
        return 0, []


if __name__ == '__main__':
    print(fetch_stocks_from_dfcf())