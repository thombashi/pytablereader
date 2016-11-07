# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import os
import tempfile

import dataproperty
import requests
from six.moves.urllib.parse import urlparse

from ._common import (
    get_extension,
    make_temp_file_path_from_url
)
from ._constant import SourceType
from ._factory import BaseTableLoaderFactory
from ._validator import UrlValidator
from .csv.core import CsvTableTextLoader
from .error import (
    InvalidFilePathError,
    InvalidUrlError,
    LoaderNotFoundError,
    HTTPError
)
from .html.core import HtmlTableTextLoader
from .interface import TableLoaderInterface
from .json.core import JsonTableTextLoader
from .markdown.core import MarkdownTableTextLoader
from .mediawiki.core import MediaWikiTableTextLoader
from .spreadsheet.excelloader import ExcelTableFileLoader


class TableUrlLoader(TableLoaderInterface):

    def __init__(self, url, format_name=None):
        self.__url = url
        loader_factory = TableUrlLoaderFactory(url)

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

    def load(self):
        return self.__loader.load()

    def inc_table_count(self):
        self.__loader.inc_table_count()


class TableUrlLoaderFactory(BaseTableLoaderFactory):

    def __init__(self, url, format_name=None):
        super(TableUrlLoaderFactory, self).__init__(None)

        self.__url = url
        self.__temp_dir_path = None

        UrlValidator(url).validate()

    def __del__(self):
        if dataproperty.is_empty_string(self.__temp_dir_path):
            return

        os.removedirs(self.__temp_dir_path)
        self.__temp_dir_path = None

    def create_from_path(self):
        """
        Create a file loader from the file extension to loading file.
        Supported file extensions are as follows:

            +----------------+-------------------------------------+
            |Format name     |         Loader                      |
            +================+=====================================+
            |``csv``         |:py:class:`~.CsvTableTextLoader`     |
            +----------------+-------------------------------------+
            |``xls``/``xlsx``|:py:class:`~.ExcelTableFileLoader`   |
            +----------------+-------------------------------------+
            |``htm``/``html``|:py:class:`~.HtmlTableTextLoader`    |
            +----------------+-------------------------------------+
            |``json``        |:py:class:`~.JsonTableTextLoader`    |
            +----------------+-------------------------------------+
            |``md``          |:py:class:`~.MarkdownTableTextLoader`|
            +----------------+-------------------------------------+

        :return:
            Loader that coincide with the file extesnion of
            :py:attr:`.source`.
        :raises pytablereader.LoaderNotFoundError:
            If appropriate file loader not found.
        """

        url_path = urlparse(self.__url).path
        try:
            url_extension = get_extension(url_path.rstrip("/"))
        except InvalidFilePathError:
            raise InvalidUrlError("url must include path")

        loader_class = self._get_loader_class(
            self._get_extension_loader_mapping(), url_extension)

        self._fetch_source(loader_class)

        return self._create_from_extension(url_extension)

    def create_from_format_name(self, format_name):
        """
        Create a file loader from a format name.
        Supported file formats are as follows:

            +---------------+--------------------------------------+
            |Format name    |         Loader                       |
            +===============+======================================+
            |``"csv"``      |:py:class:`~.CsvTableTextLoader`      |
            +---------------+--------------------------------------+
            |``"excel"``    |:py:class:`~.ExcelTableFileLoader`    |
            +---------------+--------------------------------------+
            |``"html"``     |:py:class:`~.HtmlTableTextLoader`     |
            +---------------+--------------------------------------+
            |``"json"``     |:py:class:`~.JsonTableTextLoader`     |
            +---------------+--------------------------------------+
            |``"markdown"`` |:py:class:`~.MarkdownTableTextLoader` |
            +---------------+--------------------------------------+
            |``"mediawiki"``|:py:class:`~.MediaWikiTableTextLoader`|
            +---------------+--------------------------------------+

        This method will call :py:meth:`.create_from_path` method
        if the format name is ``"auto"``.

        :param str format_name:
            Format name string or ``"auto"`` (case insensitive).
        :return: Loader that coincide with the ``format_name``:
        :raises pytablereader.LoaderNotFoundError:
            If appropriate file loader not found.
        """

        loader_class = self._get_loader_class(
            self._get_format_name_loader_mapping(), format_name)

        self._fetch_source(loader_class)

        return self._create_from_format_name(format_name)

    def _fetch_source(self, loader_class):
        loader_source_type = loader_class("").source_type

        if loader_source_type not in [SourceType.TEXT, SourceType.FILE]:
            raise ValueError(
                "unknown loader source: type={}".format(loader_source_type))

        r = requests.get(self.__url)

        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            raise HTTPError(e)

        if loader_source_type == SourceType.TEXT:
            self._source = r.text
        elif loader_source_type == SourceType.FILE:
            self.__temp_dir_path = tempfile.mkdtemp()
            self._source = "{:s}.xlsx".format(
                make_temp_file_path_from_url(self.__temp_dir_path, self.__url))
            with open(self._source, "wb") as f:
                f.write(r.content)

    def _get_common_loader_mapping(self):
        return {
            "csv": CsvTableTextLoader,
            "html": HtmlTableTextLoader,
            "json": JsonTableTextLoader,
        }

    def _get_extension_loader_mapping(self):
        """
        :return: Mappings of format-extension and loader class.
        :rtype: dict
        """

        loader_table = self._get_common_loader_mapping()
        loader_table.update({
            "htm": HtmlTableTextLoader,
            "md": MarkdownTableTextLoader,
            "xls": ExcelTableFileLoader,
            "xlsx": ExcelTableFileLoader,
        })

        return loader_table

    def _get_format_name_loader_mapping(self):
        """
        :return: Mappings of format-name and loader class.
        :rtype: dict
        """

        loader_table = self._get_common_loader_mapping()
        loader_table.update({
            "excel": ExcelTableFileLoader,
            "markdown": MarkdownTableTextLoader,
            "mediawiki": MediaWikiTableTextLoader,
        })

        return loader_table
