import os
import platform

from Stock.settings import BASE_DIR

TEMP_DIR = os.path.join(BASE_DIR, '.tmp')

RESOURCE_DIR = os.path.join(BASE_DIR, 'resource')

# 用于分离音频
if platform.system() == 'Darwin':
    RES_DIR = '/Users/yiche/Desktop/res'
else:
    RES_DIR = '/root/autodl-tmp/res'

if platform.system() == 'Darwin':
    RVC_DIR = '/Users/yiche/Desktop/weight'
else:
    RVC_DIR = '/root/autodl-tmp/rvc'

if platform.system() == 'Darwin':
    MODEL_DIR = '/Users/yiche/Desktop/weight'
else:
    MODEL_DIR = '/root/autodl-tmp/model'

if platform.system() == 'Darwin':
    SRC_DIR = '/Users/yiche/Desktop/src'
else:
    SRC_DIR = '/root/autodl-tmp/src'

if platform.system() == 'Darwin':
    OUT_DIR = '/Users/yiche/Desktop/src'
else:
    OUT_DIR = '/root/autodl-tmp/out'

if platform.system() == 'Darwin':
    DEFAULT_LEARN_SOURCE_FILE_AFTER_TRAIN = '/Users/yiche/Desktop/standard.wav'
else:
    DEFAULT_LEARN_SOURCE_FILE_AFTER_TRAIN = '/root/autodl-tmp/the_five_tigers/resource/standard.wav'

if platform.system() == 'Darwin':
    DEFAULT_UPLOAD_VIDEO = '/Users/yiche/PycharmProjects/the_five_tigers/resource/default_video.mp4'
else:
    DEFAULT_UPLOAD_VIDEO = '/root/autodl-tmp/the_five_tigers/resource/default_video.mp4'