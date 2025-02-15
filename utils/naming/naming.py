import os
import uuid
from urllib.parse import urlparse

from configs.path_config import TEMP_DIR, RES_DIR, SRC_DIR, OUT_DIR


def generate_uniq_file_name(extension: str = None) -> str:
    if extension is not None:
        if len(extension) > 0 and not extension.startswith('.'):
            extension = "." + extension
    else:
        extension = ""
    return f"{uuid.uuid4().hex}{extension}"


def generate_tmp_file_path(extension: str = None):
    return os.path.join(TEMP_DIR, generate_uniq_file_name(extension))


def generate_file_name(url):
    path = urlparse(url).path
    return os.path.basename(path)


def generate_res_path(music_shop_id, insert_middle_name='', suffix='', extension=''):
    dir_path = os.path.join(RES_DIR, insert_middle_name, music_shop_id)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return os.path.join(dir_path, f'{music_shop_id}{suffix}.{extension}')


def generate_out_dir(music_shop_id, insert_middle_name=''):
    dir_path = os.path.join(OUT_DIR, insert_middle_name, music_shop_id)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def generate_out_path(music_shop_id, insert_middle_name='', suffix='', extension=''):
    dir_path = os.path.join(OUT_DIR, insert_middle_name, music_shop_id)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if extension is not None and len(extension) > 0:
        return os.path.join(dir_path, f'{music_shop_id}{suffix}.{extension}')
    else:
        return os.path.join(dir_path, f'{music_shop_id}{suffix}')


def generate_src_path(model_id, file_suffix='', extension=None):
    file_name: str = (model_id + file_suffix + '.' + extension) if extension is not None else (model_id + file_suffix + '.wav')
    dir_path = os.path.join(SRC_DIR, model_id)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return os.path.join(dir_path, file_name)
