# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from tabledata import DataError, InvalidHeaderNameError, InvalidTableNameError

from .__version__ import __author__, __copyright__, __email__, __license__, __version__
from ._constant import PatternMatch
from ._logger import logger, set_log_level, set_logger
from .csv.core import CsvTableFileLoader, CsvTableTextLoader
from .error import (
    APIError,
    HTTPError,
    InvalidFilePathError,
    LoaderNotFoundError,
    OpenError,
    PathError,
    ProxyError,
    PypandocImportError,
    UrlError,
    ValidationError,
)
from .html.core import HtmlTableFileLoader, HtmlTableTextLoader
from .json.core import JsonTableDictLoader, JsonTableFileLoader, JsonTableTextLoader
from .jsonlines.core import JsonLinesTableFileLoader, JsonLinesTableTextLoader
from .loadermanager import TableFileLoader, TableUrlLoader
from .ltsv.core import LtsvTableFileLoader, LtsvTableTextLoader
from .markdown.core import MarkdownTableFileLoader, MarkdownTableTextLoader
from .mediawiki.core import MediaWikiTableFileLoader, MediaWikiTableTextLoader
from .spreadsheet.excelloader import ExcelTableFileLoader
from .spreadsheet.gsloader import GoogleSheetsTableLoader
from .sqlite.core import SqliteFileLoader
from .tsv.core import TsvTableFileLoader, TsvTableTextLoader
