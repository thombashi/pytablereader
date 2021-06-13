"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from mbstrdecoder import detect_file_encoding

from .._common import get_extension
from .._logger import logger
from ..csv.core import CsvTableFileLoader
from ..html.core import HtmlTableFileLoader
from ..json.core import JsonTableFileLoader
from ..jsonlines.core import JsonLinesTableFileLoader
from ..ltsv.core import LtsvTableFileLoader
from ..markdown.core import MarkdownTableFileLoader
from ..mediawiki.core import MediaWikiTableFileLoader
from ..spreadsheet.excelloader import ExcelTableFileLoader
from ..sqlite.core import SqliteFileLoader
from ..tsv.core import TsvTableFileLoader
from ._base import BaseTableLoaderFactory


class TableFileLoaderFactory(BaseTableLoaderFactory):
    """
    :param str file_path: Path to the loading file.
    :raises pytablereader.InvalidFilePathError:
        If the ``file_path`` is an empty path.
    """

    @property
    def file_extension(self):
        """
        :return: File extension of the :py:attr:`.source` (without period).
        :rtype: str
        """

        return get_extension(self.source)

    def __init__(self, source, encoding=None):
        if not encoding and source:
            encoding = detect_file_encoding(source)
            logger.debug(f"detect encoding: file={source}, encoding={encoding}")

        super().__init__(source, encoding)

    def create_from_path(self):
        """
        Create a file loader from the file extension to loading file.
        Supported file extensions are as follows:

            ==========================  =======================================
            Extension                   Loader
            ==========================  =======================================
            ``"csv"``                   :py:class:`~.CsvTableFileLoader`
            ``"xls"``/``"xlsx"``        :py:class:`~.ExcelTableFileLoader`
            ``"htm"``/``"html"``        :py:class:`~.HtmlTableFileLoader`
            ``"json"``                  :py:class:`~.JsonTableFileLoader`
            ``"jsonl"``                 :py:class:`~.JsonLinesTableFileLoader`
            ``"ldjson"``                :py:class:`~.JsonLinesTableFileLoader`
            ``"ltsv"``                  :py:class:`~.LtsvTableFileLoader`
            ``"md"``                    :py:class:`~.MarkdownTableFileLoader`
            ``"ndjson"``                :py:class:`~.JsonLinesTableFileLoader`
            ``"sqlite"``/``"sqlite3"``  :py:class:`~.SqliteFileLoader`
            ``"tsv"``                   :py:class:`~.TsvTableFileLoader`
            ==========================  =======================================

        :return:
            Loader that coincides with the file extension of the
            :py:attr:`.file_extension`.
        :raises pytablereader.LoaderNotFoundError:
            |LoaderNotFoundError_desc| loading the file.
        """

        loader = self._create_from_extension(self.file_extension)

        logger.debug(
            "TableFileLoaderFactory.create_from_path: extension={}, loader={}".format(
                self.file_extension, loader.format_name
            )
        )

        return loader

    def create_from_format_name(self, format_name):
        """
        Create a file loader from a format name.
        Supported file formats are as follows:

            ================  ======================================
            Format name               Loader
            ================  ======================================
            ``"csv"``         :py:class:`~.CsvTableFileLoader`
            ``"excel"``       :py:class:`~.ExcelTableFileLoader`
            ``"html"``        :py:class:`~.HtmlTableFileLoader`
            ``"json"``        :py:class:`~.JsonTableFileLoader`
            ``"json"``        :py:class:`~.JsonTableFileLoader`
            ``"json_lines"``  :py:class:`~.JsonTableFileLoader`
            ``"jsonl"``       :py:class:`~.JsonLinesTableFileLoader`
            ``"ltsv"``        :py:class:`~.LtsvTableFileLoader`
            ``"markdown"``    :py:class:`~.MarkdownTableFileLoader`
            ``"mediawiki"``   :py:class:`~.MediaWikiTableFileLoader`
            ``"ndjson"``      :py:class:`~.JsonLinesTableFileLoader`
            ``"sqlite"``      :py:class:`~.SqliteFileLoader`
            ``"ssv"``         :py:class:`~.CsvTableFileLoader`
            ``"tsv"``         :py:class:`~.TsvTableFileLoader`
            ================  ======================================

        :param str format_name: Format name string (case insensitive).
        :return: Loader that coincides with the ``format_name``:
        :raises pytablereader.LoaderNotFoundError:
            |LoaderNotFoundError_desc| the format.
        """

        loader = self._create_from_format_name(format_name)

        logger.debug(
            "TableFileLoaderFactory.create_from_format_name: name={}, loader={}".format(
                format_name, loader.format_name
            )
        )

        return loader

    @staticmethod
    def _get_common_loader_mapping():
        return {
            "csv": CsvTableFileLoader,
            "html": HtmlTableFileLoader,
            "json": JsonTableFileLoader,
            "jsonl": JsonLinesTableFileLoader,
            "ldjson": JsonLinesTableFileLoader,
            "ltsv": LtsvTableFileLoader,
            "ndjson": JsonLinesTableFileLoader,
            "sqlite": SqliteFileLoader,
            "tsv": TsvTableFileLoader,
        }

    def _get_extension_loader_mapping(self):
        """
        :return: Mappings of format extension and loader class.
        :rtype: dict
        """

        loader_table = self._get_common_loader_mapping()
        loader_table.update(
            {
                "htm": HtmlTableFileLoader,
                "md": MarkdownTableFileLoader,
                "sqlite3": SqliteFileLoader,
                "xlsx": ExcelTableFileLoader,
                "xls": ExcelTableFileLoader,
            }
        )

        return loader_table

    def _get_format_name_loader_mapping(self):
        """
        :return: Mappings of format name and loader class.
        :rtype: dict
        """

        loader_table = self._get_common_loader_mapping()
        loader_table.update(
            {
                "excel": ExcelTableFileLoader,
                "json_lines": JsonLinesTableFileLoader,
                "markdown": MarkdownTableFileLoader,
                "mediawiki": MediaWikiTableFileLoader,
                "ssv": CsvTableFileLoader,
            }
        )

        return loader_table
