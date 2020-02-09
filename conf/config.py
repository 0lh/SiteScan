from pathlib import Path

COROS_NUM = 320
BASE_DIR = Path.cwd()
# 定义日志路径
LOG_PATH = f'logs\\TitleScan.log'
ERROR_LOG_PATH = f'logs\\error.log'
# 定义导入的urls
URLS_FILE = f'data\\1.txt'
# 定义保存结果的路径
SAVE_FILE_01 = f'results\\01 - 正常网站.txt'
SAVE_FILE_02 = f'results\\02 - 大概率网站.txt'
SAVE_FILE_03 = f'results\\03 - 小概率网站.txt'
SAVE_FILE_04 = f'results\\04 - 异常网站.txt'
SAVE_FILE_05 = f'results\\05 - 少见响应码网站.txt'
