import os.path
from typing import TextIO

from pyzan.log import Logger


file_log = Logger(module="FILE", log_file="logs/file.log")


def open_file(file: str, mode: str) -> TextIO:
    f = open(file, mode)
    return f