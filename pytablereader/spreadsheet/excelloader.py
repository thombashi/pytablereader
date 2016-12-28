# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from six.moves import range
import xlrd

from .._validator import FileValidator
from ..error import InvalidDataError
from ..error import OpenError
from ..data import TableData
from .core import SpreadSheetLoader


class ExcelTableFileLoader(SpreadSheetLoader):
    """
    Microsoft Excel |TM| format file loader class.

    :param str file_path: Path to the loading Excel workbook file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(sheet)s``.

    .. py:attribute:: start_row

        The first row to search header row.
    """

    @property
    def format_name(self):
        return "excel"

    @property
    def _sheet_name(self):
        return self._worksheet.name

    @property
    def _row_count(self):
        return self._worksheet.nrows

    @property
    def _col_count(self):
        return self._worksheet.ncols

    def __init__(self, file_path=None):
        super(ExcelTableFileLoader, self).__init__(file_path)

        self._validator = FileValidator(file_path)

    def load(self):
        """
        Extract tabular data as |TableData| incetances from a Excel file.
        |spreadsheet_load_desc|

        :return:
            Loaded |TableData| iterator.
            |TableData| created for each sheet in the workbook.
            |load_table_name_desc|

            ===================  ====================================
            format specifier     value after the replacement
            ===================  ====================================
            ``%(filename)s``     Filename of the workbook
            ``%(sheet)s``        Name of the sheet
            ``%(format_name)s``  ``"spreadsheet"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ====================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the header row is not found.
        :raises pytablereader.error.OpenError:
            If failed to open the source file.
        """

        self._validate()

        try:
            workbook = xlrd.open_workbook(self.source)
        except xlrd.biffh.XLRDError as e:
            raise OpenError(e)

        for worksheet in workbook.sheets():
            self._worksheet = worksheet

            if self._is_empty_sheet():
                continue

            self.__extract_not_empty_col_idx()

            try:
                start_row_idx = self._get_start_row_idx()
            except InvalidDataError:
                continue

            header_list = self.__get_row_values(start_row_idx)
            record_list = [
                self.__get_row_values(row_idx)
                for row_idx in range(start_row_idx + 1, self._row_count)
            ]

            self.inc_table_count()

            yield TableData(self._make_table_name(), header_list, record_list)

    def _is_empty_sheet(self):
        return any([
            self._col_count == 0,
            self._row_count <= 1,
            # nrows == 1 means exists header row only
        ])

    def _get_start_row_idx(self):
        for row_idx in range(self.start_row, self._row_count):
            if self.__is_header_row(row_idx):
                break
        else:
            raise InvalidDataError("header row not found")

        return row_idx

    def __is_header_row(self, row_idx):
        cell_type_list = self._worksheet.row_types(
            row_idx, self._start_col_idx, self._end_col_idx + 1)
        return xlrd.XL_CELL_EMPTY not in cell_type_list

    @staticmethod
    def __is_empty_cell_type_list(cell_type_list):
        return all([
            cell_type == xlrd.XL_CELL_EMPTY
            for cell_type in cell_type_list
        ])

    def __extract_not_empty_col_idx(self):
        col_idx_list = [
            col_idx
            for col_idx in range(self._col_count)
            if not self.__is_empty_cell_type_list(
                self._worksheet.col_types(col_idx))
        ]

        self._start_col_idx = min(col_idx_list)
        self._end_col_idx = max(col_idx_list)

    def __get_row_values(self, row_idx):
        return self._worksheet.row_values(
            row_idx, self._start_col_idx, self._end_col_idx + 1)
