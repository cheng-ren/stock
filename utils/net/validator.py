import re
import mimetypes
from datetime import datetime

from django.core.validators import URLValidator, validate_email
from django.core.exceptions import ValidationError


class Validator(object):
    @staticmethod
    def is_valid_url(url):
        """
        验证是否为有效的 URL
        """
        url_validator = URLValidator()
        try:
            url_validator(url)
            return True
        except ValidationError:
            return False

    @staticmethod
    def is_valid_email(email):
        """
        验证是否为有效的邮箱地址
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def is_binary_stream(file_obj):
        """
        检查文件对象是否为二进制流
        """
        return hasattr(file_obj, 'read') and isinstance(file_obj.read(0), bytes)

    @staticmethod
    def is_valid_file_type(file_name, allowed_extensions):
        """
        验证文件类型是否符合要求
        :param file_name: 文件名
        :param allowed_extensions: 允许的文件扩展名列表（如 ['jpg', 'png', 'txt']）
        """
        file_extension = file_name.split('.')[-1].lower()
        return file_extension in allowed_extensions

    @staticmethod
    def is_valid_mime_type(file_obj, allowed_mime_types):
        """
        验证文件的 MIME 类型
        :param file_obj: 文件对象
        :param allowed_mime_types: 允许的 MIME 类型列表（如 ['image/jpeg', 'image/png']）
        """
        mime_type, _ = mimetypes.guess_type(file_obj.name)
        return mime_type in allowed_mime_types

    @staticmethod
    def is_numeric(value):
        """
        验证是否为数字
        """
        return isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit())

    @staticmethod
    def is_date(value):
        """
        验证是否为日期
        """
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False

    @staticmethod
    def matches_regex(value, pattern):
        """
        验证值是否匹配给定的正则表达式
        :param value: 待验证的值
        :param pattern: 正则表达式
        """
        return re.match(pattern, value) is not None