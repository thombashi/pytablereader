# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from collections import namedtuple
import json

import pytablewriter as ptw
import pytest

from pytablereader import (
    TableData,
    InvalidDataError,
    TableItemModifier
)

try:
    import pandas
    PANDAS_IMPORT = True
except ImportError:
    PANDAS_IMPORT = False


attr_list_2 = ["attr_a", "attr_b"]

NamedTuple2 = namedtuple("NamedTuple2", " ".join(attr_list_2))


class Test_TableData_constructor:

    __MIXED_DATA = [
        [1, 2],
        (3, 4),
        {"attr_a": 5, "attr_b": 6},
        {"attr_a": 7, "attr_b": 8, "not_exist_attr": 100},
        {"attr_a": 9},
        {"attr_b": 10},
        {},
        NamedTuple2(11, None),
    ]

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"],
        [
            [
                "normal", ["a", "b"], [[1, 2], [3, 4]],
                TableData("normal", ["a", "b"], [[1, 2], [3, 4]])
            ],
            [
                "empty_records", ["a", "b"], [],
                TableData("empty_records", ["a", "b"], [])
            ],
            [
                "empty_header", [], [[1, 2], [3, 4]],
                TableData("empty_header", [], [[1, 2], [3, 4]])
            ],
        ]
    )
    def test_normal(self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)

        print("expected: {}".format(ptw.dump_tabledata(expected)))
        print("actusl: {}".format(ptw.dump_tabledata(tabledata)))

        assert tabledata == expected

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "none_value", "expected"],
        [
            [
                "mixdata",
                attr_list_2,
                __MIXED_DATA,
                None,
                TableData("mixdata", attr_list_2, [
                    [1, 2],
                    [3, 4],
                    [5, 6],
                    [7, 8],
                    [9, None],
                    [None, 10],
                    [None, None],
                    [11, None],
                ]),
            ],
            [
                "mixdata",
                attr_list_2,
                __MIXED_DATA,
                "NULL",
                TableData("mixdata", attr_list_2, [
                    [1, 2],
                    [3, 4],
                    [5, 6],
                    [7, 8],
                    [9, "NULL"],
                    ["NULL", 10],
                    ["NULL", "NULL"],
                    [11, "NULL"],
                ]),
            ],
        ]
    )
    def test_normal_none_value(
            self, table_name, header_list, record_list, none_value, expected):
        tabledata = TableData(
            table_name, header_list, record_list,
            item_modifier=TableItemModifier(none_value=none_value))

        print("expected: {}".format(ptw.dump_tabledata(expected)))
        print("actusl: {}".format(ptw.dump_tabledata(tabledata)))

        assert tabledata == expected

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            ["tablename", ["a", "b"], [1, 2], InvalidDataError],
        ]
    )
    def test_exception(self, table_name, header_list, record_list, expected):
        with pytest.raises(expected):
            TableData(table_name, header_list, record_list)


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

    @pytest.mark.skipif("PANDAS_IMPORT is False")
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
            ["tablename", ["a", "b"], [[1, 2]], False],
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
            ["tablename", ["a", "b"], [[1, 2]], False],
        ]
    )
    def test_normal(self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)
        assert tabledata.is_empty() == expected


class Test_TableData_dumps:

    @pytest.mark.parametrize(
        [
            "table_name", "header_list", "record_list"
        ],
        [
            [
                "normal", ["a", "b"], [[1, 2], [3, 4]],
            ],
            [
                "null_header", [], [[1, 2], [3, 4]],
            ],
            [
                "null_body", ["a", "b"], [],
            ],
        ]
    )
    def test_smoke(
            self, table_name, header_list, record_list):
        tabledata = TableData(table_name, header_list, record_list)

        assert len(ptw.dump_tabledata(tabledata)) > 0
