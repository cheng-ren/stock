import json
import os.path
import platform
import time
from functools import wraps
import requests
from utils.log.yc_logger import logger
from utils.naming.naming import generate_file_name, generate_tmp_file_path
from utils.net.validator import Validator


def success_response(data=None):
    from django.http import JsonResponse
    template = {'success': True, 'message': '请求成功', 'data': data}
    return JsonResponse(template, json_dumps_params={'ensure_ascii': False})


def error_response(message):
    from django.http import JsonResponse
    if isinstance(message, Exception):
        if platform.system() == 'Darwin':
            logger.error(f"发生严重问题:{message}")
            raise message
        template = {'success': False, 'message': message.__str__(), 'data': None}
        return JsonResponse(template, status=400)
    else:
        template = {'success': False, 'message': message, 'data': None}
        return JsonResponse(template, status=400)


def require_fields(fields):
    """
    装饰器，用于检查请求中是否包含所有必需参数。
    :param fields: 必需参数的列表
    """

    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            missing_params = []
            request_params = {}
            if request.method == "POST":
                if request.content_type == 'application/json':
                    request_params = json.loads(request.body)
                else:
                    request_params = request.POST
            else:
                request_params = request.GET
            missing_params = [param for param in fields if param not in request_params]
            if missing_params and not (len(missing_params) == 1 and missing_params.__contains__('file')):
                return error_response("{}不能为空".format(', '.join(missing_params)))
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def validate_fields(validations):
    """
    装饰器，用于校验请求参数
    :param validations: 字典，定义需要校验的字段及其规则
                        示例：
                        {
                            "url": {"type": "url"},
                            "email": {"type": "email"},
                            "name": {"type": "str", "min_length": 1, "max_length": 10},
                            "age": {"type": "numeric"},
                            "file": {"type": "file", "extensions": ["jpg", "png"]},
                        }
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            errors = {}
            for field, rules in validations.items():
                value = (
                        request.GET.get(field) or
                        request.POST.get(field) or
                        (request.FILES.get(field) if "file" in rules["type"] else None)
                )

                # 跳过空值的校验（非必需字段）
                if not value:
                    continue

                # 校验逻辑
                if rules["type"] == "url" and not Validator.is_valid_url(value):
                    errors[field] = "不正确的资源地址."
                elif rules["type"] == "email" and not Validator.is_valid_email(value):
                    errors[field] = "不正确的email格式."
                elif rules["type"] == "str":
                    # 检查字符串长度
                    if not isinstance(value, str):
                        errors[field] = "类型不匹配."
                    else:
                        min_length = rules.get("min_length")
                        max_length = rules.get("max_length")
                        if min_length and len(value) < min_length:
                            errors[field] = f"不能小于 {min_length} 个字符."
                        if max_length and len(value) > max_length:
                            errors[field] = f"不能超过 {max_length} 个字符."
                elif rules["type"] == "file":
                    if not Validator.is_valid_file_type(value.name, rules.get("extensions", [])):
                        errors[field] = f"文件类型不符合要求. 允许类型: {', '.join(rules.get('extensions', []))}."
                    elif not Validator.is_binary_stream(value):
                        errors[field] = "不是二进制流."
                elif rules["type"] == "regex" and not Validator.matches_regex(value, rules["pattern"]):
                    errors[field] = f"Value does not match pattern: {rules['pattern']}."
                elif rules["type"] == "numeric" and not Validator.is_numeric(value):
                    errors[field] = "不是数值类型."
                elif rules["type"] == "date" and not Validator.is_date(value):
                    errors[field] = "不是数值类型."

            if errors:
                return error_response(errors)

            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def get_request_params(request, field, is_file=False, default=None):
    """
    批量获取请求参数，并支持类型转换和默认值。

    :param request: Django 的 HttpRequest 对象
    :param field: 参数名称
    :param is_file: 是否文件类型
    :param default: 默认值
    :return: 提取后的数值
    """

    if is_file:
        return request.FILES.get(field)

    request_params = {}
    if request.method == "POST":
        if request.content_type == 'application/json':
            request_params = json.loads(request.body)
        else:
            request_params = request.POST
    else:
        request_params = request.GET

    if field not in request_params:
        return default

    ret = request_params[field]
    if ret is None:
        return default

    return ret


def request_ai_train_server(model_id, total_epoch, file_path):
    """
    请求AI服务 - 训练
    :param model_id: 模型ID
    :param total_epoch: 迭代部署
    :param file_path: 文件路径
    :return:
    """
    start = time.time()
    logger.info(f"请求AI训练服务 - 开始 - model_id:{model_id} - total_epoch: {total_epoch}")
    data = {
        'userId': model_id,
        'totalepoch': total_epoch,
        'filePath': os.path.dirname(file_path)
    }
    url = 'http://localhost:7007/api/train'
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise Exception("Failed to call '/api/train'")
        data_dict = response.json()
        if data_dict['code'] != 200:
            raise Exception(data_dict['msg'])
    except Exception as e:
        logger.info(f"请求AI服务 - 异常 - model_id:{model_id} - {e}")
        raise e
    end = time.time()
    logger.info(f"请求AI服务 - 结束 - model_id:{model_id} 耗时:{end - start}s")


def request_ai_learn_server(vocal_file_path, model_file_path, index_file_path, learned_vocal_file_path):
    """
    请求AI服务 - 推理
    :param vocal_file_path:
    :param model_file_path:
    :param index_file_path:
    :param learned_vocal_file_path:
    :return:
    """
    start = time.time()
    logger.info(f"请求AI学习服务 - 开始")
    data = {
        'inputPath': vocal_file_path,
        'modelPath': model_file_path,
        'indexPath': index_file_path,
        'outputPath': learned_vocal_file_path
    }
    url = 'http://localhost:7007/api/convert'
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise Exception("Failed to call '/api/train'")
        data_dict = response.json()
        if data_dict['code'] != 200:
            raise Exception(data_dict['msg'])
    except Exception as e:
        raise e
    end = time.time()
    logger.info(f"请求AI学习服务 - 结束 - 耗时: {end - start}s")



def download_file(url, file_path=None) -> str:
    """
    下载文件
    :param url: 远端地址
    :param file_path: 本地存储路径
    :return:
    """
    start = time.time()
    if file_path is not None:
        dir = os.path.dirname(file_path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    if file_path is None:
        filename = generate_file_name(url)
        extension = ("." + filename.split(".")[-1]) if "." in filename else ""
        file_path = generate_tmp_file_path(extension)

    if os.path.exists(file_path):
        logger.info(f"下载文件 - 文件已存在: {file_path}")
        return file_path

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"下载文件完成: 耗时:{time.time() - start}s {file_path}")
    else:
        raise Exception("下载失败，状态码:", response.status_code)

    return file_path
