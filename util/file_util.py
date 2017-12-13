# coding=utf-8
# __author__ = 'zhiwei'
import os


def get_path(path):
    if path[0] == '~':
        path = os.path.expanduser(path)
    else:
        path = os.path.abspath(path)
    return path