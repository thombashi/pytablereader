# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import json

import pytest

from pytablereader import TableData


class Test_TableData_constructor:

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            [
                "empty_records", ["a", "b"], [],
                TableData("empty_records", ["a", "b"], [])
            ],
            [
                "normal", ["a", "b"], [[1, 2], [3, 4]],
                TableData("normal", ["a", "b"], [[1, 2], [3, 4]])
            ],
        ]
    )
    def test_normal(self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)

        print("lhs header: {}".format(tabledata.header_list))
        print("rhs header: {}".format(expected.header_list))

        assert tabledata == expected


class Test_TableData_as_dict:

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            [
                "empty_records", ["a", "b"], [],
                """{
                    "table_name": "empty_records",
                    "header_list": ["a", "b"],
                    "record_list": []
                }"""
            ],
            [
                "normal", ["a", "b"], [[1, 2], [3, 4]],
                """{
                    "table_name": "normal",
                    "header_list": ["a", "b"],
                    "record_list": [[1, 2], [3, 4]]
                }"""
            ],

        ]
    )
    def test_normal(self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)
        assert tabledata.as_dict() == json.loads(expected)


class Test_TableData_as_dataframe:

    @pytest.mark.xfail
    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list"], [
            [
                "normal", ["a", "b"], [[10, 11], [20, 21]],
            ],
        ]
    )
    def test_normal(self, table_name, header_list, record_list):
        import pandas

        tabledata = TableData(table_name, header_list, record_list)

        dataframe = pandas.DataFrame(record_list)
        dataframe.columns = header_list

        print("lhs: {}".format(tabledata.as_dataframe()))
        print("rhs: {}".format(dataframe))

        assert tabledata.as_dataframe().equals(dataframe)


class Test_TableData_hash:

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            [
                "tablename", ["a", "b"], [],
                "a7f56e50b5e19da065f90113b519e12421e8bbc2"
            ],
            [
                "tablenam", ["a", "b"], [],
                "16ba358dc22c0827cad275087d3daa4952d7fe10"
            ],
            [
                "tablename", ["a", "c"], [],
                "9091fdf20816c2790f51eced4a95c8a33131699e"
            ],
            [
                "tablename", ["a", "b"], [1, 2],
                "9503bdae29a7a696e9c65460c7877489f3d00440"
            ],
        ]
    )
    def test_normal(self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)
        assert tabledata.__hash__() == expected


class Test_TableData_is_empty_header:

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            ["tablename", [], [], True],
            ["tablename", ["a", "b"], [], False],
            ["tablename", [], [1, 2], True],
            ["tablename", ["a", "b"], [1, 2], False],
        ]
    )
    def test_normal(self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)
        assert tabledata.is_empty_header() == expected


class Test_TableData_is_empty_record:

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            ["tablename", [], [], True],
            ["tablename", ["a", "b"], [], True],
            ["tablename", [], [1, 2], False],
            ["tablename", ["a", "b"], [1, 2], False],
        ]
    )
    def test_normal(self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)
        assert tabledata.is_empty_record() == expected


class Test_TableData_is_empty:

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            ["tablename", [], [], True],
            ["tablename", ["a", "b"], [], True],
            ["tablename", [], [1, 2], True],
            ["tablename", ["a", "b"], [1, 2], False],
        ]
    )
    def test_normal(self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)
        assert tabledata.is_empty() == expected


class Test_TableData_dumps:

    @pytest.mark.parametrize(
        [
            "table_name", "header_list", "record_list", "expected"
        ],
        [
            [
                "normal", ["a", "b"], [[1, 2], [3, 4]],
                ""
            ],
        ]
    )
    def test_smoke(
            self, table_name, header_list, record_list,
            expected):
        tabledata = TableData(table_name, header_list, record_list)

        assert len(tabledata.dumps()) > 0
