# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import csv
import io
import platform

import dataproperty as dp
from mbstrdecoder import MultiByteStrDecoder
import pathvalidate
import six

from .._constant import (
    SourceType,
    TableNameTemplate as tnt
)
from .._validator import (
    FileValidator,
    TextValidator
)
from ..error import InvalidDataError
from ..interface import TableLoader
from .formatter import CsvTableFormatter


class CsvTableLoader(TableLoader):
    """
    Abstract class of CSV table loader.

    .. py:attribute:: header_list

        Attribute names of the table. Use the first line of
        the csv file as attribute list if header_list is empty.

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

    def __init__(self, source):
        super(CsvTableLoader, self).__init__(source)

        self._csv_reader = None

        self.header_list = ()
        self.delimiter = ","
        self.quotechar = '"'
        self.encoding = "utf-8"

    @property
    def format_name(self):
        return "csv"

    def _to_data_matrix(self):
        try:
            return [
                [self.__modify_item(data) for data in row]
                for row in self._csv_reader
                if dp.is_not_empty_sequence(row)
            ]
        except csv.Error as e:
            raise InvalidDataError(e)

    def __modify_item(self, data):
        inttype = dp.IntegerType(data)
        if inttype.is_convertible_type():
            return inttype.convert()

        floattype = dp.FloatType(data)
        if floattype.is_convertible_type():
            return data

        return MultiByteStrDecoder(data).unicode_str


class CsvTableFileLoader(CsvTableLoader):
    """
    CSV format file loader class.

    :param str file_path: Path to the loading CSV file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s``.
    """

    def __init__(self, file_path):
        super(CsvTableFileLoader, self).__init__(file_path)

        self._validator = FileValidator(file_path)

    def load(self):
        """
        Extract tabular data as |TableData| incetances from a CSV file.
        |load_source_desc_file|

        :return:
            Loaded table data.
            |load_table_name_desc|

            ===================  ========================================
            format specifier     value after the replacement
            ===================  ========================================
            ``%(filename)s``     |filename_desc|
            ``%(format_name)s``  ``"csv"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ========================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the CSV data is invalid.

        .. seealso::
            :py:func:`csv.reader`
        """

        self._validate()
        pathvalidate.validate_file_path(self.source)

        if all([
            platform.system() == "Windows",
            six.PY3
        ]):
            self._csv_reader = csv.reader(
                io.open(self.source, "r", encoding=self.encoding),
                delimiter=self.delimiter, quotechar=self.quotechar,
                strict=True, skipinitialspace=True)
        else:
            self._csv_reader = csv.reader(
                open(self.source, "r"),
                delimiter=self.delimiter, quotechar=self.quotechar,
                strict=True, skipinitialspace=True)

        formatter = CsvTableFormatter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return tnt.FILENAME


class CsvTableTextLoader(CsvTableLoader):
    """
    CSV format text loader class.

    :param str text: CSV text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(format_name)s%(format_id)s``.
    """

    def __init__(self, text):
        super(CsvTableTextLoader, self).__init__(text)

        self._validator = TextValidator(text)

    def load(self):
        """
        Extract tabular data as |TableData| incetances from a CSV text object.
        |load_source_desc_text|

        :return:
            Loaded table data.
            |load_table_name_desc|

            ===================  ========================================
            format specifier     value after the replacement
            ===================  ========================================
            ``%(filename)s``     ``""``
            ``%(format_name)s``  ``"csv"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ========================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the CSV data is invalid.

        .. seealso::
            :py:func:`csv.reader`
        """

        self._validate()

        self._csv_reader = csv.reader(
            six.StringIO(self.source.strip()),
            delimiter=self.delimiter, quotechar=self.quotechar,
            strict=True, skipinitialspace=True)
        formatter = CsvTableFormatter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}{:s}".format(tnt.FORMAT_NAME, tnt.FORMAT_ID)
