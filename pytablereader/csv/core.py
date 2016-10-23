# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import csv

from dataproperty.type import FloatTypeChecker
import pathvalidate
import six

from .._constant import SourceType
from .._constant import TableNameTemplate as tnt
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
    def _format_name(self):
        return "csv"

    def _to_data_matrix(self):
        return [
            [
                six.b(data).decode(self.encoding, "ignore")
                if not FloatTypeChecker(data).is_type() else data
                for data in row
            ]
            for row in self._csv_reader
        ]


class CsvTableFileLoader(CsvTableLoader):
    """
    Concrete class of CSV file loader.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s``.
    """

    @property
    def source_type(self):
        return SourceType.FILE

    def __init__(self, file_path):
        super(CsvTableFileLoader, self).__init__(file_path)

    def load(self):
        """
        Extract |TableData| from a CSV file.
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

        self._csv_reader = csv.reader(
            open(self.source, "r"),
            delimiter=self.delimiter, quotechar=self.quotechar)
        formatter = CsvTableFormatter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return tnt.FILENAME


class CsvTableTextLoader(CsvTableLoader):
    """
    Concrete class of CSV text loader.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(format_name)s%(format_id)s``.
    """

    @property
    def source_type(self):
        return SourceType.TEXT

    def __init__(self, text):
        super(CsvTableTextLoader, self).__init__(text)

    def load(self):
        """
        Extract table data from a CSV text.
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
            delimiter=self.delimiter, quotechar=self.quotechar)
        formatter = CsvTableFormatter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}{:s}".format(tnt.FORMAT_NAME, tnt.FORMAT_ID)
