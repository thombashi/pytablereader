# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .._common import get_extension
from ..csv.core import CsvTableFileLoader
from ..html.core import HtmlTableFileLoader
from ..json.core import JsonTableFileLoader
from ..markdown.core import MarkdownTableFileLoader
from ..mediawiki.core import MediaWikiTableFileLoader
from ..spreadsheet.excelloader import ExcelTableFileLoader
from ..tsv.core import TsvTableFileLoader
from ._base import BaseTableLoaderFactory


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

            ================  =====================================
            Format name                Loader                      
            ================  =====================================
            ``csv``           :py:class:`~.CsvTableFileLoader`     
            ``xls``/``xlsx``  :py:class:`~.ExcelTableFileLoader`   
            ``htm``/``html``  :py:class:`~.HtmlTableFileLoader`    
            ``json``          :py:class:`~.JsonTableFileLoader`    
            ``md``            :py:class:`~.MarkdownTableFileLoader`
            ================  =====================================

        :return:
            Loader that coincide with the file extesnion of the
            :py:attr:`.file_extension`.
        :raises pytablereader.LoaderNotFoundError:
            If appropriate file loader not found.
        """

        return self._create_from_extension(self.file_extension)

    def create_from_format_name(self, format_name):
        """
        Create a file loader from a format name.
        Supported file formats are as follows:

            ===============  ======================================
            Format name               Loader                       
            ===============  ======================================
            ``"csv"``        :py:class:`~.CsvTableFileLoader`      
            ``"excel"``      :py:class:`~.ExcelTableFileLoader`    
            ``"html"``       :py:class:`~.HtmlTableFileLoader`     
            ``"json"``       :py:class:`~.JsonTableFileLoader`     
            ``"markdown"``   :py:class:`~.MarkdownTableFileLoader` 
            ``"mediawiki"``  :py:class:`~.MediaWikiTableFileLoader`
            ===============  ======================================

        :param str format_name: Format name string (case insensitive).
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
            "tsv": TsvTableFileLoader,
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
