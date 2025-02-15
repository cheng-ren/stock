import hashlib
import os
import shutil
from pathlib import Path

from utils.log.yc_logger import logger


# 替换文件中固定文本
def replace_text_in_file(file_path, old_text, new_text):
    """
    替换一个文件中的文本
    :param file_path: 文件路径
    :param old_text: 旧文本
    :param new_text: 新文本
    :return: None
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 替换指定文本
        updated_content = content.replace(old_text, new_text)

        # 将更新后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        logger.info(f"已成功将 '{old_text}' 替换为 '{new_text}'")
    except Exception as e:
        logger.error(f"替换过程中出错: {e}")


def md5_hash(text):
    """
    MD5
    :param text: 文本内容
    :return: md5值
    """
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()


def save_tmp_file(file, file_path):
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    logger.info(f"保存流到文件:{file_path}")


def find_file_in_folder(folder_path, regex) -> str:
    """
    在指定文件夹中查找特定文件名的文件。

    :param folder_path: 文件夹路径
    :param regex: 要查找的文件名
    :return: 文件的完整路径，找不到返回 None
    """
    logger.info(f"查找 - 开始 - {folder_path} - {regex}")

    search_path = Path(folder_path)
    files = list(search_path.rglob(regex))
    if len(files) == 0:
        logger.info(f"查找 - 结束 - 未找到 - {regex}")
    else:
        ret = files[0].__str__()
        logger.info(f"查找 - 结束 - 找到 - {regex} - {ret}")
        return ret
    return None


def copy(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copy(src, dst)


def move(src, dst):
    if os.path.exists(dst):
        os.remove(dst)
    shutil.move(src, dst)


def remove_all_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # 删除文件或符号链接
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 删除目录及其内容
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def remove_file(file_path):
    """
    删除文件
    :param file_path: 文件路径
    :return:
    """
    if file_path is None:
        return
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    else:
        if os.path.exists(file_path):
            os.remove(file_path)
        logger.info(f"删除文件: {file_path}")


def md5_file(file_path):
    """计算文件的 MD5 值"""
    md5_hash_f = hashlib.md5()  # 创建一个 MD5 对象
    try:
        with open(file_path, 'rb') as file:  # 以二进制模式打开文件
            # 分块读取文件内容，适用于大文件
            while chunk := file.read(8192):  # 每次读取 8KB
                md5_hash_f.update(chunk)
        return md5_hash_f.hexdigest()  # 返回 MD5 值的十六进制表示
    except FileNotFoundError:
        return "文件未找到"
    except Exception as e:
        return f"计算 MD5 时出错: {e}"


def find_uniq_file(folder_path) -> str:
    # 获取文件夹中的所有文件（包括隐藏文件，忽略子目录）
    files = [f for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, f)) and not f.startswith(".")]

    if len(files) == 1:
        return os.path.join(folder_path, files[0])
    elif len(files) == 0:
        print("The folder is empty.")
        return None
    else:
        print("The folder contains multiple files.")
        return None