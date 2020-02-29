"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import enum


class Default:
    ENCODING = "utf-8"


class SourceType:
    TEXT = "text"
    FILE = "file"
    URL = "url"
    OBJECT = "object"


class TableNameTemplate:
    __FORMAT = "%({:s})s"
    DEFAULT = __FORMAT.format("default")
    FILENAME = __FORMAT.format("filename")
    FORMAT_NAME = __FORMAT.format("format_name")
    FORMAT_ID = __FORMAT.format("format_id")
    GLOBAL_ID = __FORMAT.format("global_id")
    KEY = __FORMAT.format("key")
    TITLE = __FORMAT.format("title")
    SHEET = __FORMAT.format("sheet")


@enum.unique
class PatternMatch(enum.Enum):
    OR = 0
    AND = 1
