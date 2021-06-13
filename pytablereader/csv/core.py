"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import csv
import io
import warnings

import typepy
from mbstrdecoder import MultiByteStrDecoder

from pytablereader import DataError

from .._common import get_file_encoding
from .._constant import TableNameTemplate as tnt
from .._logger import FileSourceLogger, TextSourceLogger
from .._validator import FileValidator, TextValidator
from ..interface import AbstractTableReader
from .formatter import CsvTableFormatter


class CsvTableLoader(AbstractTableReader):
    """
    The abstract class of CSV table loaders.

    .. py:attribute:: headers

        Attribute names of the table. Use the first line of
        the CSV file as attribute list if ``headers`` is empty.

    .. py:attribute:: delimiter

        A one-character string used to separate fields.
        Defaults to ``","``.

    .. py:attribute:: quotechar

        A one-character string used to quote fields containing
        special characters, such as the ``delimiter`` or ``quotechar``,
        or which contain new-line characters.
        Defaults to ``'"'``.

    .. py:attribute:: encoding

        Encoding of the CSV data.
    """

    @property
    def format_name(self):
        return "csv"

    @property
    def delimiter(self):
        # "delimiter" must be a string, not an unicode
        return str(MultiByteStrDecoder(self.__delimiter).unicode_str)

    @delimiter.setter
    def delimiter(self, value):
        self.__delimiter = value

    @property
    def quotechar(self):
        # "quotechar" must be a string, not an unicode
        return str(MultiByteStrDecoder(self.__quotechar).unicode_str)

    @quotechar.setter
    def quotechar(self, value):
        self.__quotechar = value

    @property
    def header_list(self):
        warnings.warn("'header_list' has moved to 'headers'", DeprecationWarning)
        return self.headers

    @header_list.setter
    def header_list(self, value):
        warnings.warn("'header_list' has moved to 'headers'", DeprecationWarning)
        self.headers = value

    def __init__(self, source, quoting_flags, type_hints, type_hint_rules):
        super().__init__(source, quoting_flags, type_hints, type_hint_rules)

        self._csv_reader = None

        self.headers = ()
        self.delimiter = ","
        self.quotechar = '"'
        self.encoding = None

    def _to_data_matrix(self):
        try:
            return [
                [self.__modify_item(data, col) for col, data in enumerate(row)]
                for row in self._csv_reader
                if typepy.is_not_empty_sequence(row)
            ]
        except (csv.Error, UnicodeDecodeError) as e:
            raise DataError(e)

    def __modify_item(self, data, col: int):
        if self.type_hints and (col in self.type_hints):
            try:
                return self.type_hints[col](data).convert()
            except typepy.TypeConversionError:
                pass

        return MultiByteStrDecoder(data).unicode_str


class CsvTableFileLoader(CsvTableLoader):
    """
    A file loader class to extract tabular data from CSV files.

    :param str file_path: Path to the loading CSV file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s``.

    :Examples:
        :ref:`example-csv-table-loader`
    """

    def __init__(self, file_path, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(file_path, quoting_flags, type_hints, type_hint_rules)

        self._validator = FileValidator(file_path)
        self._logger = FileSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a CSV file.
        |load_source_desc_file|

        :return:
            Loaded table data.
            |load_table_name_desc|

            ===================  ========================================
            Format specifier     Value after the replacement
            ===================  ========================================
            ``%(filename)s``     |filename_desc|
            ``%(format_name)s``  ``"csv"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ========================================
        :rtype: |TableData| iterator
        :raises pytablereader.DataError:
            If the CSV data is invalid.

        .. seealso::
            :py:func:`csv.reader`
        """

        self._validate()
        self._logger.logging_load()
        self.encoding = get_file_encoding(self.source, self.encoding)

        self._csv_reader = csv.reader(
            open(self.source, encoding=self.encoding),
            delimiter=self.delimiter,
            quotechar=self.quotechar,
            strict=True,
            skipinitialspace=True,
        )

        formatter = CsvTableFormatter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return tnt.FILENAME


class CsvTableTextLoader(CsvTableLoader):
    """
    A text loader class to extract tabular data from CSV text data.

    :param str text: CSV text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(format_name)s%(format_id)s``.

    :Examples:
        :ref:`example-csv-table-loader`
    """

    def __init__(self, text, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(text, quoting_flags, type_hints, type_hint_rules)

        self._validator = TextValidator(text)
        self._logger = TextSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a CSV text object.
        |load_source_desc_text|

        :return:
            Loaded table data.
            |load_table_name_desc|

            ===================  ========================================
            Format specifier     Value after the replacement
            ===================  ========================================
            ``%(filename)s``     ``""``
            ``%(format_name)s``  ``"csv"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ========================================
        :rtype: |TableData| iterator
        :raises pytablereader.DataError:
            If the CSV data is invalid.

        .. seealso::
            :py:func:`csv.reader`
        """

        self._validate()
        self._logger.logging_load()

        self._csv_reader = csv.reader(
            io.StringIO(self.source.strip()),
            delimiter=self.delimiter,
            quotechar=self.quotechar,
            strict=True,
            skipinitialspace=True,
        )
        formatter = CsvTableFormatter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return f"{tnt.FORMAT_NAME:s}{tnt.FORMAT_ID:s}"
