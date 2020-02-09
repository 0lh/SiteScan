import argparse
import sys
from conf.config import URLS_FILE, COROS_NUM


def parse_args():
    parser = argparse.ArgumentParser(usage='python3 scan.py --urls [source urls file]')
    parser.add_argument("--urls", "-u", type=str, help="source urls file.")
    # parser.add_argument("--coros", "-c", default=COROS_NUM, type=int, help="coros num")
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    args = parser.parse_args()
    return args
