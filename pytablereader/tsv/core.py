# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from .._validator import (
    FileValidator,
    TextValidator
)
from ..csv.core import (
    CsvTableFileLoader,
    CsvTableTextLoader
)


class TsvTableFileLoader(CsvTableFileLoader):
    """
    Concrete class of a table file loader for
    tab separated values (TSV) format.

    :param str file_path: Path to the loading TSV file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s``.
    """

    def __init__(self, file_path):
        super(TsvTableFileLoader, self).__init__(file_path)

        self.delimiter = "\t"

        self._validator = FileValidator(file_path)


class TsvTableTextLoader(CsvTableTextLoader):
    """
    Concrete class of a table text loader for
    tab separated values (TSV) format.

    :param str text: TSV text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(format_name)s%(format_id)s``.
    """

    def __init__(self, text):
        super(TsvTableTextLoader, self).__init__(text)

        self.delimiter = "\t"

        self._validator = TextValidator(text)
