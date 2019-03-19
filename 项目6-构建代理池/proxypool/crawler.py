import json
import re

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0

class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')