# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from .interface import TableLoaderInterface
from .error import (
    LoaderNotFoundError,
)
from .factory import TableUrlLoaderFactory


class TableUrlLoader(TableLoaderInterface):
    """
    Loader class to loading tables from URL.

    :param str url: URL to load.
    :param str format_name: Defaults to |None|.
    :param dict proxies: Defaults to |None|.

        .. seealso::
            - `requests proxies <http://requests-docs-ja.readthedocs.io/en/latest/user/advanced/#proxies>`__
    """

    def __init__(self, url, format_name=None, proxies=None):
        self.__url = url
        self.__proxies = proxies

        loader_factory = TableUrlLoaderFactory(url, proxies)

        try:
            self.__loader = loader_factory.create_from_format_name(format_name)
        except (LoaderNotFoundError, ValueError):
            self.__loader = loader_factory.create_from_path()

    @property
    def format_name(self):
        return self.__loader.format_name

    @property
    def source_type(self):
        return self.__loader.source_type

    @property
    def encoding(self):
        try:
            return self.__loader.encoding
        except AttributeError:
            return None

    def load(self):
        return self.__loader.load()

    def inc_table_count(self):
        self.__loader.inc_table_count()
