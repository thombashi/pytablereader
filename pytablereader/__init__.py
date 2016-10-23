# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from .error import ValidationError
from .error import InvalidDataError
from .error import OpenError
from .error import InvalidTableNameError

import pytablereader.data
import pytablereader.error

from .data import TableData

from .csv.core import CsvTableFileLoader
from .csv.core import CsvTableTextLoader
from .html.core import HtmlTableFileLoader
from .html.core import HtmlTableTextLoader
from .mediawiki.core import MediaWikiTableFileLoader
from .mediawiki.core import MediaWikiTableTextLoader
from .spreadsheet.excelloader import ExcelTableFileLoader
from .json.core import JsonTableFileLoader
from .json.core import JsonTableTextLoader
