# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import pytest

import pytablereader as ptr
from pytablereader.data import TableData
from pytablereader._tabledata_sanitizer import SQLiteTableDataSanitizer


class Test_SQLiteTableDataSanitizer:

    @pytest.mark.parametrize(
        [
            "table_name", "header_list", "record_list", "expected"
        ],
        [
            [
                "normal", ["a", "b"], [[1, 2], [3, 4]],
                TableData("normal", ["a", "b"], [[1, 2], [3, 4]])
            ],
            [
                "OFFSET", ["abort", "ASC"], [[1, 2], [3, 4]],
                TableData("OFFSET", ["abort", "ASC"], [[1, 2], [3, 4]])
            ],
            [
                r"a!b\c#d$e%f&g'h(i)j",
                [r"a!b\c#d$e%f&g'h(i)j", r"k@l[m]n{o}p;q:r,s.t/u\\v"],
                [[1, 2], [3, 4]],
                TableData(
                    "abcdefghij",
                    ["abcdefghij", "klmnopqrstuv"], [[1, 2], [3, 4]])
            ],
            [
                "ALL", ["and", "Index"], [[1, 2], [3, 4]],
                TableData(
                    "rename_ALL",
                    ["rename_and", "rename_Index"], [[1, 2], [3, 4]])
            ],
            [
                "0invalid_tn", ["1invalid", "where"], [[1, 2], [3, 4]],
                TableData(
                    "rename_0invalid_tn",
                    ["rename_1invalid", "rename_where"], [[1, 2], [3, 4]])
            ],
        ]
    )
    def test_normal(
            self, table_name, header_list, record_list,
            expected):
        tabledata = TableData(table_name, header_list, record_list)
        sanitizer = SQLiteTableDataSanitizer(tabledata)
        new_tabledata = sanitizer.sanitize()

        print("lhs: {}".format(new_tabledata.dumps()))
        print("rhs: {}".format(expected.dumps()))

        assert new_tabledata == expected

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            ["", ["a", "b"], [], ptr.InvalidTableNameError],
            [None, ["a", "b"], [], ptr.InvalidTableNameError],
            ["dummy", ["", "b"], [], ptr.InvalidHeaderNameError],
            ["dummy", ["a", None], [], ptr.InvalidHeaderNameError],
        ]
    )
    def test_exception_invalid_data(
            self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)
        sanitizer = SQLiteTableDataSanitizer(tabledata)

        with pytest.raises(expected):
            sanitizer.sanitize()
