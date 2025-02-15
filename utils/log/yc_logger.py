import logging
import time
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timezone, timedelta
import os

# 确保日志目录存在
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")


# __name__ 模块logger，对应settings中的 名称为：'' 的 logger
logger = logging.getLogger(__name__)
logger.propagate = False  # 禁用继承
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # 设置控制台日志级别

# 创建文件处理器
file_handler = TimedRotatingFileHandler(
    log_filename,  # 日志文件基础名称
    when="midnight",  # 时间间隔，支持 'S', 'M', 'H', 'D', 'midnight', 'W0-W6'
    interval=1,       # 每隔 1 天
    backupCount=7,    # 保留最近 7 天的日志文件
    encoding='utf-8'  # 日志文件编码
)
file_handler.setLevel(logging.DEBUG)  # 设置文件日志级别

class TimezoneFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        tz = timezone(timedelta(hours=8))  # UTC+8 (上海时间)
        record_time = datetime.fromtimestamp(record.created, tz)
        if datefmt:
            return record_time.strftime(datefmt)
        return record_time.isoformat()


# 定义日志格式
formatter = TimezoneFormatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 示例日志记录
logger.debug("这是调试日志")
logger.info("这是信息日志")
logger.warning("这是警告日志")
logger.error("这是错误日志")
logger.critical("这是严重错误日志")