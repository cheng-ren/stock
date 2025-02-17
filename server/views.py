import json
from collections import defaultdict
from datetime import datetime

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from utils.log.yc_logger import logger
from utils.net.net import require_fields, validate_fields, get_request_params, success_response, error_response
from database_stock.exec import query_news_from_database, query_stock_from_database

def index(request):
    return render(request, 'server.html')


@require_http_methods(["GET"])
@require_fields(['code', 'keyword', 'start_time', 'end_time'])
@validate_fields({'code': {"type": "str", "min_length": 5}, 'keyword': {"type": "str"}, 'start_time': {"type": "date"}, 'end_time': {"type": "date"}})
def query_news(request):
    stock_code = get_request_params(request, field='code')
    logger.info(stock_code)
    keyword = get_request_params(request, field='keyword')
    start_time = get_request_params(request, field='start_time')
    end_time = get_request_params(request, field='end_time')
    try:
        result = query_news_from_database(stock_code, keyword, start_time, end_time)

        format_result = []
        for item in result:
            ret_item = None
            if isinstance(item['list'], list):
                ret_item = item
            elif isinstance(item['list'], str):
                item['list'] = json.loads(item['list'])
                ret_item = item

            if ret_item is not None:
                for it in item['list']:
                    time_str = it['publish_time']
                    dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
                    formatted_str = dt.strftime('%m-%d %H:%M')
                    it['publish_time'] = formatted_str

                format_result.append(ret_item)


        return success_response({"datas": format_result})
    except Exception as e:
        return error_response(e)


@require_http_methods(["GET"])
@require_fields(['keyword'])
@validate_fields({'keyword': {"type": "str", "min_length": 1}})
def query_stock(request):
    keyword = get_request_params(request, field='keyword')
    try:
        ret = query_stock_from_database(keyword)
        return success_response({"count": len(ret), "datas": ret})
    except Exception as e:
        return error_response(e)

