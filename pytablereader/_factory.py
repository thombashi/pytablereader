# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._common import get_extension
from .csv.core import CsvTableFileLoader
from .error import LoaderNotFoundError
from .html.core import HtmlTableFileLoader
from .json.core import JsonTableFileLoader
from .markdown.core import MarkdownTableFileLoader
from .mediawiki.core import MediaWikiTableFileLoader
from .spreadsheet.excelloader import ExcelTableFileLoader


@six.add_metaclass(abc.ABCMeta)
class BaseTableLoaderFactory(object):

    @property
    def source(self):
        """
        :return: Data source to load.
        :rtype: str
        """

        return self._source

    def __init__(self, source):
        self._source = source

    @abc.abstractmethod
    def create_from_path(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def create_from_format_name(self, format_name):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _get_extension_loader_mapping(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _get_format_name_loader_mapping(self):  # pragma: no cover
        pass

    def get_format_name_list(self):
        """
        :return: Available format name List.
        :rtype: list
        """

        return sorted(self._get_format_name_loader_mapping())

    def get_extension_list(self):
        """
        :return: Available format-extension list.
        :rtype: list
        """

        return sorted(self._get_extension_loader_mapping())

    def _get_loader_class(self, loader_mapping, format_name):
        try:
            format_name = format_name.lower()
        except AttributeError:
            raise ValueError("format name must be a string")

        try:
            return loader_mapping[format_name]
        except KeyError:
            raise LoaderNotFoundError(", ".join([
                "loader not found: format='{}'".format(format_name),
                "source='{}'".format(self.source),
            ]))

    def _create_from_extension(self, extension):
        try:
            return self._get_loader_class(
                self._get_extension_loader_mapping(), extension)(self.source)
        except LoaderNotFoundError as e:
            raise LoaderNotFoundError("\n".join([
                "{:s} (unknown extension).".format(e.args[0]),
                "",
                "acceptable extensions are: {}.".format(
                    ", ".join(self.get_extension_list())),
            ]))

    def _create_from_format_name(self, format_name):
        if format_name.lower() == "auto":
            return self.create_from_path()

        try:
            return self._get_loader_class(
                self._get_format_name_loader_mapping(), format_name)(self.source)
        except LoaderNotFoundError as e:
            raise LoaderNotFoundError("\n".join([
                "{:s} (unknown format name).".format(e.args[0]),
                "acceptable format names are: {}.".format(
                    ", ".join(self.get_format_name_list())),
            ]))


class TableFileLoaderFactory(BaseTableLoaderFactory):
    """
    :param str file_path: Path to the loading file.
    :raises pytablereader.InvalidFilePathError:
        If the ``file_path`` is a empty path.
    """

    @property
    def file_extension(self):
        """
        :return: File extension of the :py:attr:`.source` (without period).
        :rtype: str
        """

        return get_extension(self.source)

    def create_from_path(self):
        """
        Create a file loader from the file extension to loading file.
        Supported file extensions are as follows:

            +----------------+-------------------------------------+
            |Format name     |         Loader                      |
            +================+=====================================+
            |``csv``         |:py:class:`~.CsvTableFileLoader`     |
            +----------------+-------------------------------------+
            |``xls``/``xlsx``|:py:class:`~.ExcelTableFileLoader`   |
            +----------------+-------------------------------------+
            |``htm``/``html``|:py:class:`~.HtmlTableFileLoader`    |
            +----------------+-------------------------------------+
            |``json``        |:py:class:`~.JsonTableFileLoader`    |
            +----------------+-------------------------------------+
            |``md``          |:py:class:`~.MarkdownTableFileLoader`|
            +----------------+-------------------------------------+

        :return:
            Loader that coincide with the file extesnion of
            :py:attr:`.source`.
        :raises pytablereader.LoaderNotFoundError:
            If appropriate file loader not found.
        """

        return self._create_from_extension(self.file_extension)

    def create_from_format_name(self, format_name):
        """
        Create a file loader from a format name.
        Supported file formats are as follows:

            +---------------+--------------------------------------+
            |Format name    |         Loader                       |
            +===============+======================================+
            |``"csv"``      |:py:class:`~.CsvTableFileLoader`      |
            +---------------+--------------------------------------+
            |``"excel"``    |:py:class:`~.ExcelTableFileLoader`    |
            +---------------+--------------------------------------+
            |``"html"``     |:py:class:`~.HtmlTableFileLoader`     |
            +---------------+--------------------------------------+
            |``"json"``     |:py:class:`~.JsonTableFileLoader`     |
            +---------------+--------------------------------------+
            |``"markdown"`` |:py:class:`~.MarkdownTableFileLoader` |
            +---------------+--------------------------------------+
            |``"mediawiki"``|:py:class:`~.MediaWikiTableFileLoader`|
            +---------------+--------------------------------------+

        This method will call :py:meth:`.create_from_path` method
        if the format name is ``"auto"``.

        :param str format_name:
            Format name string or ``"auto"`` (case insensitive).
        :return: Loader that coincide with the ``format_name``:
        :raises pytablereader.LoaderNotFoundError:
            If appropriate file loader not found.
        """

        return self._create_from_format_name(format_name)

    def _get_common_loader_mapping(self):
        return {
            "csv": CsvTableFileLoader,
            "html": HtmlTableFileLoader,
            "json": JsonTableFileLoader,
        }

    def _get_extension_loader_mapping(self):
        """
        :return: Mappings of format-extension and loader class.
        :rtype: dict
        """

        loader_table = self._get_common_loader_mapping()
        loader_table.update({
            "htm": HtmlTableFileLoader,
            "md": MarkdownTableFileLoader,
            "xlsx": ExcelTableFileLoader,
            "xls": ExcelTableFileLoader,
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
            "markdown": MarkdownTableFileLoader,
            "mediawiki": MediaWikiTableFileLoader,
        })

        return loader_table
