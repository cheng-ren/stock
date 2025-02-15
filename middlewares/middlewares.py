import json
import time
import urllib

from django.utils.deprecation import MiddlewareMixin

from utils.log.yc_logger import logger


class LogMiddle(MiddlewareMixin):
    # 日志处理中间件
    def process_request(self, request):
        # 存放请求过来时的时间
        self.start_time = time.time()
        message = ''
        if request.method == "GET":
            message = '接收到请求 %s %s %s' % (request.path, request.method, request.GET)
        elif request.method == "POST":
            request_params = None
            if request.content_type == 'application/json':
                request_params = json.loads(request.body)
            else:
                request_params = request.POST
            message = '接收到请求 %s %s %s' % (request.path, request.method, request_params)
        logger.info(message)
        return None

    def process_response(self, request, response):
        """响应完成后触发"""
        try:
            end_time = time.time()
            # 请求路径
            path = request.path
            # 请求方式
            method = request.method
            # 响应状态码
            status_code = response.status_code
            # 响应内容
            content = response.content
            # 记录信息
            content = str(content.decode('utf-8'))
            content = urllib.parse.unquote(content)
            content = (json.loads(content))
            message = '%s %s %s %s 耗时:%ss' % (path, method, status_code, content, (end_time - self.start_time))
            logger.info(message)
        except:
            logger.critical('系统错误')
        return response

    def process_exception(self, request, exception):
        """捕获异常"""
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 请求路径
        path = request.path
        # 请求方式
        method = request.method

        message = '%s %s %s %s' % (localtime, path, method, exception)
        logger.error(message)
        # print("这是错误处理。。。%s" % exception)
