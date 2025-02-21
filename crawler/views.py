from datetime import datetime

from crawler.utils.browser import fetch_html_content_by
from crawler.utils.haiguitouzi import fetch_stocks_from_hgtz
from database_stock.exec import sync_news, sync_stock, query_stock_from_database, query_news_group_stock_from_database
import requests
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from crawler.utils.dongfangcaifu import fetch_news_from_dfcf, fetch_stocks_from_dfcf
from utils.log.yc_logger import logger
from utils.net.net import require_fields, get_request_params, validate_fields, success_response, error_response


def index(request):
    return render(request, 'crawler.html')


@require_http_methods(["GET"])
def stock_list(request):
    # 会产生股票代码和股票名称
    sync_to_database = get_request_params(request, field='sync_to_database', default=False)
    items = fetch_stocks_from_hgtz()
    if sync_to_database:
        for item in items:
            sync_stock(item)
    return success_response({"count": len(items), "datas": items})


def automatic_first_of_day(request):
    """
    获取所有股票码后 拉取资讯
    :return: 查询结果
    """
    try:
        stocks = query_stock_from_database("", is_limit=False)
        format_result = []
        for stock in stocks:
            count, items = fetch_news_from_dfcf(stock_code=stock['code'])
            for item in items:
                sync_news(item)
            format_result.append({"code": stock['code'], "title": stock['title'], "count": count})
            logger.info(f"{len(format_result)}/{len(stocks)} -- code: {stock['code']} - title: {stock['title']} - count: {count}")
        return success_response(format_result)
    except Exception as e:
        return error_response(e)


def automatic_every_hour_of_day(request):
    """
       获取所有股票码后 拉取资讯
       :return: 查询结果
       """
    try:
        stocks = query_news_group_stock_from_database()
        format_result = []
        for stock in stocks:
            count, items = fetch_news_from_dfcf(stock_code=stock['code'])
            for item in items:
                sync_news(item)
            format_result.append({"code": stock['code'], "title": stock['title'], "count": count})
            logger.info(
                f"{len(format_result)}/{len(stocks)} -- code: {stock['code']} - title: {stock['title']} - count: {count}")
        return success_response(format_result)
    except Exception as e:
        return error_response(e)

@require_http_methods(["GET"])
@require_fields(['code'])
@validate_fields({'code': {"type": "numeric"}})
def stock_by_id(request):
    """
    根据股票代码获取资讯数据
    :param code: 股票ID
    :param fetch_end_time: 向前探索的日期 eg:2025-01-09 00:00:00
    :param sync_to_database: 是否同步数据库
    :return: 查询结果
    """
    try:
        stock_code = get_request_params(request, field='code')
        fetch_end_time = get_request_params(request, field='fetch_end_time', default=None)
        sync_to_database = get_request_params(request, field='sync_to_database', default=False)
        count, items = fetch_news_from_dfcf(stock_code=stock_code, fetch_end_time=fetch_end_time)
        if sync_to_database:
            for item in items:
                sync_news(item)
        return success_response({"count": count, "datas": items})
    except Exception as e:
        return error_response(e)