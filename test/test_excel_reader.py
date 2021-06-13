"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest
import xlsxwriter
from pytablewriter import dumps_tabledata
from tabledata import TableData

import pytablereader as ptr
from pytablereader.interface import AbstractTableReader


def write_worksheet(worksheet, table):
    for row_idx, row in enumerate(table):
        for col_idx, item in enumerate(row):
            worksheet.write(row_idx, col_idx, item)


@pytest.fixture
def valid_excel_file_path(tmpdir):
    test_file_path = tmpdir.join("tmp.xlsx")
    workbook = xlsxwriter.Workbook(str(test_file_path))

    write_worksheet(
        workbook.add_worksheet("boolsheet"),
        table=[
            ["true", "false", "tf", "lost"],
            ["True", "False", "True", "True"],
            ["true", "false", "False", ""],
            ["TRUE", "FALSE", "False", "False"],
        ],
    )

    write_worksheet(
        workbook.add_worksheet("testsheet1"),
        table=[
            ["", "", "", ""],
            ["", "a1", "b1", "c1"],
            ["", "aa1", "ab1", "ac1"],
            ["", 1, 1.1, "a"],
            ["", 2, 2.2, "bb"],
            ["", 3, 3.3, "cc"],
        ],
    )

    worksheet = workbook.add_worksheet("testsheet2")  # noqa: W0612

    write_worksheet(
        workbook.add_worksheet("testsheet3"),
        table=[
            ["", "", ""],
            ["", "", ""],
            ["a3", "b3", "c3"],
            ["aa3", "ab3", "ac3"],
            [4, 1.1, "a"],
            [5, "", "bb"],
            [6, 3.3, ""],
        ],
    )

    write_worksheet(
        workbook.add_worksheet("invalid_sheet"),
        table=[["", "", "", ""], ["", "a", "", "c"], ["", "aa", "ab", ""], ["", "", 1.1, "a"]],
    )

    workbook.close()

    return str(test_file_path)


@pytest.fixture
def invalid_excel_file_path(tmpdir):
    test_file_path = tmpdir.join("invalid.xlsx")
    workbook = xlsxwriter.Workbook(str(test_file_path))

    write_worksheet(
        workbook.add_worksheet("testsheet1"),
        table=[["", "", "", ""], ["", "a", "", "c"], ["", "aa", "ab", ""], ["", "", 1.1, "a"]],
    )

    worksheet = workbook.add_worksheet("testsheet2")  # noqa: W0612

    workbook.close()

    return str(test_file_path)


@pytest.mark.xfail(run=False)
class Test_ExcelTableFileLoader_make_table_name:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @property
    def monkey_property(self):
        return "testsheet"

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(sheet)s", "/path/to/data.xlsx", "testsheet"],
            ["%(filename)s", "/path/to/data.xlsx", "data"],
            ["prefix_%(filename)s_%(sheet)s", "/path/to/data.xlsx", "prefix_data_testsheet"],
            ["%(format_name)s%(format_id)s_%(filename)s", "/path/to/data.xlsx", "excel0_data"],
        ],
    )
    def test_normal(self, monkeypatch, value, source, expected):
        loader = ptr.ExcelTableFileLoader(source)
        loader.table_name = value

        monkeypatch.setattr(ptr.ExcelTableFileLoader, "_sheet_name", self.monkey_property)

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            [None, "/path/to/data.xlsx", ValueError],
            ["", "/path/to/data.xlsx", ValueError],
            ["%(sheet)s", None, ptr.InvalidTableNameError],
            ["%(sheet)s", "", ptr.InvalidTableNameError],
        ],
    )
    def test_exception(self, value, source, expected):
        loader = ptr.ExcelTableFileLoader(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


@pytest.mark.xfail(run=False)
class Test_ExcelTableFileLoader_load:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["table_name", "start_row", "expected_list"],
        [
            [
                "%(sheet)s",
                0,
                [
                    TableData(
                        "boolsheet",
                        ["true", "false", "tf", "lost"],
                        [
                            [True, False, True, True],
                            [True, False, False, ""],
                            [True, False, False, False],
                        ],
                    ),
                    TableData(
                        "testsheet1",
                        ["a1", "b1", "c1"],
                        [
                            ["aa1", "ab1", "ac1"],
                            [1.0, 1.1, "a"],
                            [2.0, 2.2, "bb"],
                            [3.0, 3.3, "cc"],
                        ],
                    ),
                    TableData(
                        "testsheet3",
                        ["a3", "b3", "c3"],
                        [["aa3", "ab3", "ac3"], [4.0, 1.1, "a"], [5.0, "", "bb"], [6.0, 3.3, ""]],
                    ),
                ],
            ],
            [
                "%(filename)s_%(sheet)s",
                2,
                [
                    TableData("tmp_boolsheet", ["TRUE", "FALSE", "False", "False"], []),
                    TableData(
                        "tmp_testsheet1",
                        ["aa1", "ab1", "ac1"],
                        [[1.0, 1.1, "a"], [2.0, 2.2, "bb"], [3.0, 3.3, "cc"]],
                    ),
                    TableData(
                        "tmp_testsheet3",
                        ["a3", "b3", "c3"],
                        [["aa3", "ab3", "ac3"], [4.0, 1.1, "a"], [5.0, "", "bb"], [6.0, 3.3, ""]],
                    ),
                ],
            ],
        ],
    )
    def test_normal(self, valid_excel_file_path, table_name, start_row, expected_list):
        loader = ptr.ExcelTableFileLoader(valid_excel_file_path)
        loader.table_name = table_name
        loader.start_row = start_row

        for table_data in loader.load():
            print(f"[actual]\n{dumps_tabledata(table_data)}")
            assert table_data.in_tabledata_list(expected_list)

    @pytest.mark.parametrize(
        ["table_name", "start_row", "expected"], [["%(sheet)s", 0, ptr.DataError]]
    )
    def test_abnormal(self, invalid_excel_file_path, table_name, start_row, expected):
        loader = ptr.ExcelTableFileLoader(invalid_excel_file_path)
        loader.table_name = table_name
        loader.start_row = start_row

        for tabletuple in loader.load():
            assert tabletuple == []

    @pytest.mark.parametrize(
        ["source", "expected"], [["", ptr.InvalidFilePathError], [None, ptr.InvalidFilePathError]]
    )
    def test_null_file_path(self, source, expected):
        loader = ptr.ExcelTableFileLoader(source)

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(["table_name", "expected"], [["", ValueError], [None, ValueError]])
    def test_null_table_name(self, valid_excel_file_path, table_name, expected):
        loader = ptr.ExcelTableFileLoader(valid_excel_file_path)
        loader.table_name = table_name

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
