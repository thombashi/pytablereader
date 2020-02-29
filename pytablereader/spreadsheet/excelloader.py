"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from tabledata import TableData

from pytablereader import DataError

from .._logger import FileSourceLogger
from .._validator import FileValidator
from ..error import OpenError
from .core import SpreadSheetLoader


class ExcelTableFileLoader(SpreadSheetLoader):
    """
    A file loader class to extract tabular data from Microsoft Excel |TM|
    files.

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

    def __init__(self, file_path=None, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(file_path, quoting_flags, type_hints, type_hint_rules)

        self._validator = FileValidator(file_path)
        self._logger = FileSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from an Excel file.
        |spreadsheet_load_desc|

        :return:
            Loaded |TableData| iterator.
            |TableData| created for each sheet in the workbook.
            |load_table_name_desc|

            ===================  ====================================
            Format specifier     Value after the replacement
            ===================  ====================================
            ``%(filename)s``     Filename of the workbook
            ``%(sheet)s``        Name of the sheet
            ``%(format_name)s``  ``"spreadsheet"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ====================================
        :rtype: |TableData| iterator
        :raises pytablereader.DataError:
            If the header row is not found.
        :raises pytablereader.error.OpenError:
            If failed to open the source file.
        """

        try:
            import excelrd as xlrd
        except ImportError:
            import xlrd

        self._validate()
        self._logger.logging_load()

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
            except DataError:
                continue

            rows = [
                self.__get_row_values(row_idx)
                for row_idx in range(start_row_idx + 1, self._row_count)
            ]

            self.inc_table_count()
            headers = self.__get_row_values(start_row_idx)

            yield TableData(
                self._make_table_name(),
                headers,
                rows,
                dp_extractor=self.dp_extractor,
                type_hints=self._extract_type_hints(headers),
            )

    def _is_empty_sheet(self):
        return any(
            [
                self._col_count == 0,
                self._row_count <= 1,
                # nrows == 1 means exists header row only
            ]
        )

    def _get_start_row_idx(self):
        for row_idx in range(self.start_row, self._row_count):
            if self.__is_header_row(row_idx):
                break
        else:
            raise DataError("header row not found")

        return row_idx

    def __is_header_row(self, row_idx):
        try:
            from excelrd import XL_CELL_EMPTY
        except ImportError:
            from xlrd import XL_CELL_EMPTY

        return XL_CELL_EMPTY not in self._worksheet.row_types(
            row_idx, self._start_col_idx, self._end_col_idx + 1
        )

    @staticmethod
    def __is_empty_cell_types(cell_types):
        try:
            from excelrd import XL_CELL_EMPTY
        except ImportError:
            from xlrd import XL_CELL_EMPTY

        return all([cell_type == XL_CELL_EMPTY for cell_type in cell_types])

    def __extract_not_empty_col_idx(self):
        col_idx_list = [
            col_idx
            for col_idx in range(self._col_count)
            if not self.__is_empty_cell_types(self._worksheet.col_types(col_idx))
        ]

        self._start_col_idx = min(col_idx_list)
        self._end_col_idx = max(col_idx_list)

    def __get_row_values(self, row_idx):
        return self._worksheet.row_values(row_idx, self._start_col_idx, self._end_col_idx + 1)
