"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from ..interface import TableLoaderInterface


class TableLoaderManager(TableLoaderInterface):
    def __init__(self, loader):
        self.__loader = loader

    @property
    def loader(self):
        return self.__loader

    @property
    def format_name(self):
        return self.__loader.format_name

    @property
    def source_type(self):
        return self.__loader.source_type

    @property
    def table_name(self):
        return self.__loader.table_name

    @table_name.setter
    def table_name(self, value):
        self.__loader.table_name = value

    @property
    def encoding(self):
        try:
            return self.__loader.encoding
        except AttributeError:
            return None

    @encoding.setter
    def encoding(self, codec_name):
        self.__loader.encoding = codec_name

    @property
    def type_hints(self):
        return self.__loader.type_hints

    @type_hints.setter
    def type_hints(self, value):
        self.__loader.type_hints = value

    def load(self):
        return self.__loader.load()

    def inc_table_count(self):
        self.__loader.inc_table_count()
