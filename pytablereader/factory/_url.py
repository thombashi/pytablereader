# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import os
import tempfile

import typepy
from six.moves.urllib.parse import urlparse

from .._common import get_extension, make_temp_file_path_from_url
from .._constant import SourceType
from .._logger import logger
from .._validator import UrlValidator
from ..csv.core import CsvTableFileLoader, CsvTableTextLoader
from ..error import HTTPError, InvalidFilePathError, ProxyError, UrlError
from ..html.core import HtmlTableTextLoader
from ..json.core import JsonTableTextLoader
from ..jsonlines.core import JsonLinesTableTextLoader
from ..ltsv.core import LtsvTableTextLoader
from ..markdown.core import MarkdownTableTextLoader
from ..mediawiki.core import MediaWikiTableTextLoader
from ..spreadsheet.excelloader import ExcelTableFileLoader
from ..sqlite.core import SqliteFileLoader
from ..tsv.core import TsvTableTextLoader
from ._base import BaseTableLoaderFactory


class TableUrlLoaderFactory(BaseTableLoaderFactory):
    @property
    def __url(self):
        return self._source

    def __init__(self, url, encoding=None, proxies=None):
        super(TableUrlLoaderFactory, self).__init__(url, encoding)

        self.__proxies = proxies
        self.__temp_dir_path = None

        UrlValidator(url).validate()

    def __del__(self):
        if typepy.is_null_string(self.__temp_dir_path):
            return

        os.removedirs(self.__temp_dir_path)
        self.__temp_dir_path = None

    def create_from_path(self):
        """
        Create a file loader from the file extension to loading file.
        Supported file extensions are as follows:

            =========================================  =====================================
            Extension                                  Loader
            =========================================  =====================================
            ``"csv"``                                  :py:class:`~.CsvTableTextLoader`
            ``"xls"``/``"xlsx"``                       :py:class:`~.ExcelTableFileLoader`
            ``"htm"``/``"html"``/``"asp"``/``"aspx"``  :py:class:`~.HtmlTableTextLoader`
            ``"json"``                                 :py:class:`~.JsonTableTextLoader`
            ``"jsonl"``/``"ldjson"``/``"ndjson"``      :py:class:`~.JsonLinesTableTextLoader`
            ``"ltsv"``                                 :py:class:`~.LtsvTableTextLoader`
            ``"md"``                                   :py:class:`~.MarkdownTableTextLoader`
            ``"sqlite"``/``"sqlite3"``                 :py:class:`~.SqliteFileLoader`
            ``"tsv"``                                  :py:class:`~.TsvTableTextLoader`
            =========================================  =====================================

        :return:
            Loader that coincides with the file extension of the URL.
        :raises pytablereader.UrlError: If unacceptable URL format.
        :raises pytablereader.LoaderNotFoundError:
            |LoaderNotFoundError_desc| loading the URL.
        """

        import requests

        url_path = urlparse(self.__url).path
        try:
            url_extension = get_extension(url_path.rstrip("/"))
        except InvalidFilePathError:
            raise UrlError("url must include path")

        logger.debug("TableUrlLoaderFactory: extension={}".format(url_extension))

        loader_class = self._get_loader_class(self._get_extension_loader_mapping(), url_extension)

        try:
            self._fetch_source(loader_class)
        except requests.exceptions.ProxyError as e:
            raise ProxyError(e)

        loader = self._create_from_extension(url_extension)

        logger.debug("TableUrlLoaderFactory: loader={}".format(loader.format_name))

        return loader

    def create_from_format_name(self, format_name):
        """
        Create a file loader from a format name.
        Supported file formats are as follows:

            ==========================  ======================================
            Format name                 Loader
            ==========================  ======================================
            ``"csv"``                   :py:class:`~.CsvTableTextLoader`
            ``"excel"``                 :py:class:`~.ExcelTableFileLoader`
            ``"html"``                  :py:class:`~.HtmlTableTextLoader`
            ``"json"``                  :py:class:`~.JsonTableTextLoader`
            ``"json_lines"``            :py:class:`~.JsonLinesTableTextLoader`
            ``"jsonl"``                 :py:class:`~.JsonLinesTableTextLoader`
            ``"ldjson"``                :py:class:`~.JsonLinesTableTextLoader`
            ``"ltsv"``                  :py:class:`~.LtsvTableTextLoader`
            ``"markdown"``              :py:class:`~.MarkdownTableTextLoader`
            ``"mediawiki"``             :py:class:`~.MediaWikiTableTextLoader`
            ``"ndjson"``                :py:class:`~.JsonLinesTableTextLoader`
            ``"sqlite"``                :py:class:`~.SqliteFileLoader`
            ``"ssv"``                   :py:class:`~.CsvTableFileLoader`
            ``"tsv"``                   :py:class:`~.TsvTableTextLoader`
            ==========================  ======================================

        :param str format_name: Format name string (case insensitive).
        :return: Loader that coincide with the ``format_name``:
        :raises pytablereader.LoaderNotFoundError:
            |LoaderNotFoundError_desc| the format.
        :raises TypeError: If ``format_name`` is not a string.
        """

        import requests

        logger.debug("TableUrlLoaderFactory: name={}".format(format_name))

        loader_class = self._get_loader_class(self._get_format_name_loader_mapping(), format_name)

        try:
            self._fetch_source(loader_class)
        except requests.exceptions.ProxyError as e:
            raise ProxyError(e)

        loader = self._create_from_format_name(format_name)

        logger.debug("TableUrlLoaderFactory: loader={}".format(loader.format_name))

        return loader

    def _fetch_source(self, loader_class):
        import requests
        import retryrequests

        loader_source_type = loader_class("").source_type

        if loader_source_type not in [SourceType.TEXT, SourceType.FILE]:
            raise ValueError("unknown loader source: type={}".format(loader_source_type))

        r = retryrequests.get(self.__url, proxies=self.__proxies)

        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            raise HTTPError(e)

        if typepy.is_null_string(self._encoding):
            self._encoding = r.encoding

        logger.debug(
            "\n".join(
                [
                    "_fetch_source: ",
                    "  source-type={}".format(loader_source_type),
                    "  content-type={}".format(r.headers["Content-Type"]),
                    "  encoding={}".format(self._encoding),
                    "  status-code={}".format(r.status_code),
                ]
            )
        )

        if loader_source_type == SourceType.TEXT:
            self._source = r.text
        elif loader_source_type == SourceType.FILE:
            self.__temp_dir_path = tempfile.mkdtemp()
            self._source = "{:s}.xlsx".format(
                make_temp_file_path_from_url(self.__temp_dir_path, self.__url)
            )
            with open(self._source, "wb") as f:
                f.write(r.content)

    def _get_common_loader_mapping(self):
        return {
            "csv": CsvTableTextLoader,
            "html": HtmlTableTextLoader,
            "json": JsonTableTextLoader,
            "jsonl": JsonLinesTableTextLoader,
            "ldjson": JsonLinesTableTextLoader,
            "ltsv": LtsvTableTextLoader,
            "ndjson": JsonLinesTableTextLoader,
            "sqlite": SqliteFileLoader,
            "tsv": TsvTableTextLoader,
        }

    def _get_extension_loader_mapping(self):
        """
        :return: Mappings of format-extension and loader class.
        :rtype: dict
        """

        loader_table = self._get_common_loader_mapping()
        loader_table.update(
            {
                "asp": HtmlTableTextLoader,
                "aspx": HtmlTableTextLoader,
                "htm": HtmlTableTextLoader,
                "md": MarkdownTableTextLoader,
                "sqlite3": SqliteFileLoader,
                "xls": ExcelTableFileLoader,
                "xlsx": ExcelTableFileLoader,
            }
        )

        return loader_table

    def _get_format_name_loader_mapping(self):
        """
        :return: Mappings of format-name and loader class.
        :rtype: dict
        """

        loader_table = self._get_common_loader_mapping()
        loader_table.update(
            {
                "excel": ExcelTableFileLoader,
                "json_lines": JsonLinesTableTextLoader,
                "markdown": MarkdownTableTextLoader,
                "mediawiki": MediaWikiTableTextLoader,
                "ssv": CsvTableFileLoader,
            }
        )

        return loader_table
