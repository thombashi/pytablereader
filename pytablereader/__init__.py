# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from .error import ValidationError
from .error import InvalidTableNameError
from .error import InvalidHeaderNameError
from .error import InvalidFilePathError
from .error import InvalidDataError
from .error import EmptyDataError
from .error import OpenError
from .error import LoaderNotFoundError

from .data import TableData

from ._tabledata_sanitizer import TableDataSanitizer
from ._tabledata_sanitizer import SQLiteTableDataSanitizer

from .csv.core import CsvTableFileLoader
from .csv.core import CsvTableTextLoader
from .html.core import HtmlTableFileLoader
from .html.core import HtmlTableTextLoader
from .markdown.core import MarkdownTableFileLoader
from .markdown.core import MarkdownTableTextLoader
from .mediawiki.core import MediaWikiTableFileLoader
from .mediawiki.core import MediaWikiTableTextLoader
from .spreadsheet.excelloader import ExcelTableFileLoader
from .json.core import JsonTableFileLoader
from .json.core import JsonTableTextLoader

from ._factory import TableFileLoaderFactory
