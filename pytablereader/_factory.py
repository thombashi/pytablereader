# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import copy
import os

import dataproperty

from .error import InvalidFilePathError
from .error import LoaderNotFoundError

from .csv.core import CsvTableFileLoader
from .html.core import HtmlTableFileLoader
from .json.core import JsonTableFileLoader
from .markdown.core import MarkdownTableFileLoader
from .mediawiki.core import MediaWikiTableFileLoader
from .spreadsheet.excelloader import ExcelTableFileLoader


class FileLoaderFactory(object):
    """
    :param str file_path: File path to loading.
    :raises pytablereader.InvalidFilePathError:
        If the ``file_path`` is a empty path.
    """

    __COMMON_LOADER_TABLE = {
        "csv": CsvTableFileLoader,
        "html": HtmlTableFileLoader,
        "json": JsonTableFileLoader,
    }

    @property
    def file_path(self):
        """
        :return: File path to loading.
        :rtype: str
        """

        return self.__file_path

    @property
    def file_extension(self):
        """
        :return: File extension of the :py:attr:`.file_path` (without period).
        :rtype: str
        """

        return self.__file_extension

    def __init__(self, file_path):
        self.__file_path = file_path

        self.__validate()

        self.__file_extension = os.path.splitext(self.file_path)[1].lstrip(".")

    def create_from_file_path(self):
        """
        Create a file loader from file extension to loading.

        :return: Loader that coincide with the :py:attr:`.file_path`.
        :raises pytablereader.LoaderNotFoundError:
            If appropriate file loader not found.
        """

        try:
            return self.__create_loader(
                self.get_extension_loader_mapping(), self.file_extension)
        except LoaderNotFoundError as e:
            raise LoaderNotFoundError("\n".join([
                "{:s} (unknown file extension).".format(e.args[0]),
                "",
                "acceptable file extensions are: {}.".format(
                    ", ".join(sorted(self.get_extension_loader_mapping()))),
                "",
                "or specify destination file format with '--from' option.",
                "acceptable file formats to '--from' options are: {}.".format(
                    ", ".join(sorted(self.get_format_name_loader_mapping()))),
            ]))

    def create_from_format_name(self, format_name):
        """
        Create a file loader from file extension to loading.

        :return:
            Loader that coincide with the ``format_name``:

            +-----------+---------------------------------------------------+
            |Format name|         Loader                                    |
            +===========+===================================================+
            |csv        |:py:class:`~pytablereader.CsvTableFileLoader`      |
            +-----------+---------------------------------------------------+
            |excel      |:py:class:`~pytablereader.ExcelTableFileLoader`    |
            +-----------+---------------------------------------------------+
            |html       |:py:class:`~pytablereader.HtmlTableFileLoader`     |
            +-----------+---------------------------------------------------+
            |json       |:py:class:`~pytablereader.JsonTableFileLoader`     |
            +-----------+---------------------------------------------------+
            |markdown   |:py:class:`~pytablereader.MarkdownTableFileLoader` |
            +-----------+---------------------------------------------------+
            |mediawiki  |:py:class:`~pytablereader.MediaWikiTableFileLoader`|
            +-----------+---------------------------------------------------+
        :raises |LoaderNotFoundError|: If appropriate file loader not found.
        """

        if format_name == "auto":
            return self.create_from_file_path()

        try:
            return self.__create_loader(
                self.get_format_name_loader_mapping(), format_name)
        except LoaderNotFoundError as e:
            raise LoaderNotFoundError("\n".join([
                "{:s} (unknown file format).".format(e.args[0]),
                "specify destination file format with '--to' option.",
                "acceptable file formats to '--to' options are: {}.".format(
                    ", ".join(sorted(self.get_format_name_loader_mapping()))),
            ]))

    def __validate(self):
        if dataproperty.is_empty_string(self.file_path):
            raise InvalidFilePathError("file path is empty")

    def __create_loader(self, loader_table, format_name):
        try:
            return loader_table[format_name](self.file_path)
        except KeyError:
            raise LoaderNotFoundError(", ".join([
                "loader not found: format='{:s}'".format(format_name),
                "path='{:s}'".format(self.file_path),
            ]))

    @classmethod
    def get_format_name_loader_mapping(self):
        """
        :return: Mappings of format-name and loader class.
        :rtype: dict
        """

        loader_table = copy.deepcopy(self.__COMMON_LOADER_TABLE)
        loader_table.update({
            "excel": ExcelTableFileLoader,
            "markdown": MarkdownTableFileLoader,
            "mediawiki": MediaWikiTableFileLoader,
        })

        return loader_table

    @classmethod
    def get_extension_loader_mapping(self):
        """
        :return: Mappings of format-extension and loader class.
        :rtype: dict
        """

        loader_table = copy.deepcopy(
            self.__COMMON_LOADER_TABLE)
        loader_table .update({
            "htm": HtmlTableFileLoader,
            "md": MarkdownTableFileLoader,
            "xlsx": ExcelTableFileLoader,
            "xls": ExcelTableFileLoader,
        })

        return loader_table
