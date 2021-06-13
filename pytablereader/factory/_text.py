"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from .._logger import logger
from ..csv.core import CsvTableTextLoader
from ..html.core import HtmlTableTextLoader
from ..json.core import JsonTableTextLoader
from ..jsonlines.core import JsonLinesTableTextLoader
from ..ltsv.core import LtsvTableTextLoader
from ..markdown.core import MarkdownTableTextLoader
from ..mediawiki.core import MediaWikiTableTextLoader
from ..tsv.core import TsvTableTextLoader
from ._base import BaseTableLoaderFactory


class TableTextLoaderFactory(BaseTableLoaderFactory):
    def create_from_path(self):
        raise NotImplementedError()

    def create_from_format_name(self, format_name):
        """
        Create a file loader from a format name.
        Supported file formats are as follows:

            ==========================  ======================================
            Format name                 Loader
            ==========================  ======================================
            ``"csv"``                   :py:class:`~.CsvTableTextLoader`
            ``"html"``                  :py:class:`~.HtmlTableTextLoader`
            ``"json"``                  :py:class:`~.JsonTableTextLoader`
            ``"json_lines"``            :py:class:`~.JsonLinesTableTextLoader`
            ``"jsonl"``                 :py:class:`~.JsonLinesTableTextLoader`
            ``"ldjson"``                :py:class:`~.JsonLinesTableTextLoader`
            ``"ltsv"``                  :py:class:`~.LtsvTableTextLoader`
            ``"markdown"``              :py:class:`~.MarkdownTableTextLoader`
            ``"mediawiki"``             :py:class:`~.MediaWikiTableTextLoader`
            ``"ndjson"``                :py:class:`~.JsonLinesTableTextLoader`
            ``"ssv"``                   :py:class:`~.CsvTableTextLoader`
            ``"tsv"``                   :py:class:`~.TsvTableTextLoader`
            ==========================  ======================================

        :param str format_name: Format name string (case insensitive).
        :return: Loader that coincide with the ``format_name``:
        :raises pytablereader.LoaderNotFoundError:
            |LoaderNotFoundError_desc| the format.
        :raises TypeError: If ``format_name`` is not a string.
        """

        loader = self._create_from_format_name(format_name)

        logger.debug(f"TableTextLoaderFactory: name={format_name}, loader={loader.format_name}")

        return loader

    def _get_common_loader_mapping(self):
        return {
            "csv": CsvTableTextLoader,
            "html": HtmlTableTextLoader,
            "json": JsonTableTextLoader,
            "jsonl": JsonLinesTableTextLoader,
            "ldjson": JsonLinesTableTextLoader,
            "ltsv": LtsvTableTextLoader,
            "ndjson": JsonLinesTableTextLoader,
            "tsv": TsvTableTextLoader,
        }

    def _get_extension_loader_mapping(self):
        """
        :return: Mappings of format-extension and loader class.
        :rtype: dict
        """

        loader_table = self._get_common_loader_mapping()
        loader_table.update({"htm": HtmlTableTextLoader, "md": MarkdownTableTextLoader})

        return loader_table

    def _get_format_name_loader_mapping(self):
        """
        :return: Mappings of format-name and loader class.
        :rtype: dict
        """

        loader_table = self._get_common_loader_mapping()
        loader_table.update(
            {
                "json_lines": JsonLinesTableTextLoader,
                "markdown": MarkdownTableTextLoader,
                "mediawiki": MediaWikiTableTextLoader,
                "ssv": CsvTableTextLoader,
            }
        )

        return loader_table
