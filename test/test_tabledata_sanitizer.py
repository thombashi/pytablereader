# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals

import pytablewriter as ptw
import pytest

import pytablereader as ptr
from pytablereader import TableData
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
                "all_missing_header", [], [[1, 2], [3, 4]],
                TableData(
                    "all_missing_header",
                    ["complement_attr_0", "complement_attr_1"],
                    [[1, 2], [3, 4]])
            ],
            [
                "part_missing_header", ["", "b", None], [],
                TableData(
                    "part_missing_header",
                    ["complement_attr_0", "b", "complement_attr_2"], [])
            ],
            [
                r"@a!b\c#d$e%f&g'h(i)j_",
                [r"a!b\c#d$e%f&g'h(i)j", r"k@l[m]n{o}p;q:r,s.t/u\\v"],
                [[1, 2], [3, 4]],
                TableData(
                    "a_b_c_d_e_f_g_h_i_j",
                    ["abcdefghij", "klmnopqrstuv"], [[1, 2], [3, 4]])
            ],
            [  # SQLite reserved keywords
                "ALL", ["and", "Index"], [[1, 2], [3, 4]],
                TableData(
                    "rename_ALL",
                    ["and", "Index"], [[1, 2], [3, 4]])
            ],
            [
                "0invalid_tn", ["1invalid", "where"], [[1, 2], [3, 4]],
                TableData(
                    "rename_0invalid_tn",
                    ["rename_1invalid", "where"], [[1, 2], [3, 4]])
            ],
            [
                "Python (programming language) - Wikipedia, the free encyclopedia.html",
                ["a b", "c d"], [[1, 2], [3, 4]],
                TableData(
                    "Python_programming_language_Wikipedia_the_free_encyclopedia_html",
                    ["ab", "cd"], [[1, 2], [3, 4]])
            ],
            [
                "multibyte csv",
                ["姓", "名", "生年月日", "郵便番号", "住所", "電話番号"],
                [
                    ["山田", "太郎", "2001/1/1", "100-0002",
                        "東京都千代田区皇居外苑", "03-1234-5678"],
                    ["山田", "次郎", "2001/1/2", "251-0036",
                        "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
                ],
                TableData(
                    "multibyte_csv",
                    ["姓", "名", "生年月日", "郵便番号", "住所", "電話番号"],
                    [
                        ["山田", "太郎", "2001/1/1", "100-0002",
                         "東京都千代田区皇居外苑", "03-1234-5678"],
                        ["山田", "次郎", "2001/1/2", "251-0036",
                         "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
                    ])
            ],
        ]
    )
    def test_normal(
            self, table_name, header_list, record_list,
            expected):
        tabledata = TableData(table_name, header_list, record_list)
        sanitizer = SQLiteTableDataSanitizer(tabledata)
        new_tabledata = sanitizer.sanitize()

        print("lhs: {}".format(ptw.dump_tabledata(new_tabledata)))
        print("rhs: {}".format(ptw.dump_tabledata(expected)))

        assert new_tabledata == expected

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            ["", ["a", "b"], [], ptr.InvalidTableNameError],
            [None, ["a", "b"], [], ptr.InvalidTableNameError],
            ["dummy", [], [], ptr.EmptyDataError],
        ]
    )
    def test_exception_invalid_data(
            self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)
        sanitizer = SQLiteTableDataSanitizer(tabledata)

        with pytest.raises(expected):
            sanitizer.sanitize()
