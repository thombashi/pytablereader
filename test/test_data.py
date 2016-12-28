# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals
from collections import namedtuple
from decimal import Decimal
import json

import dataproperty as dp
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


class Test_TableData_eq:

    __DATA_0 = TableData(
        "Sheet1",
        [
            'i', 'f', 'c', 'if', 'ifc', 'bool',
            'inf', 'nan', 'mix_num', 'time',
        ],
        [
            [
                1, "1.1", 'aa', 1, 1, 'True',
                float("inf"), "nan", 1,
                '2017-01-01T00:00:00',
            ],
            [
                2, "2.2", 'bbb', "2.2", "2.2", 'False',
                float("inf"), float("NaN"), float("inf"),
                '2017-01-02 03:04:05+09:00',
            ],
            [
                3, "3.33", 'cccc', -3, 'ccc', 'True',
                float("inf"), float("NaN"), float("NaN"),
                '2017-01-01T00:00:00',
            ],
        ])

    __DATA_1 = TableData(
        "tablename",
        ["a", "b", "c", "dd", "e"],
        []
    )

    @pytest.mark.parametrize(["lhs",  "rhs", "expected"], [
        [__DATA_0, __DATA_0, True],
        [__DATA_0, __DATA_1, False],
    ])
    def test_normal(self, lhs, rhs, expected):
        assert (lhs == rhs) == expected


class Test_TableData_as_dict:

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            [
                "normal", ["a", "b"], [[1, 2], [3, 4]],
                """{"normal": [{"a": 1, "b": 2}, {"a": 3, "b": 4}]}"""
            ],
            [
                "number", ["a", "b"], [[1, 2.0], [3.3, Decimal("4.4")]],
                """{"number": [{"a": 1, "b": 2}, {"a": 3.3, "b": 4.4}]}"""
            ],
            [
                "include_none",
                ["a", "b"],
                [[None, 2], [None, None], [3, None], [None, None]],
                """{"include_none": [{"b": 2}, {"a": 3}]}"""
            ],
            [
                "empty_records", ["a", "b"], [],
                """{"empty_records": []}"""
            ],

        ]
    )
    def test_normal(self, table_name, header_list, record_list, expected):
        tabledata = TableData(table_name, header_list, record_list)
        assert tabledata.as_dict() == json.loads(expected)

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list", "expected"], [
            ["none_header", None, [[1, 2], [3, 4]], TypeError],
            ["none_records", ["a", "b"], None, TypeError],
        ]
    )
    def test_exception(self, table_name, header_list, record_list, expected):
        with pytest.raises(expected):
            TableData(table_name, header_list, record_list).as_dict()


class Test_TableData_as_dataframe:

    @pytest.mark.skipif("PANDAS_IMPORT is False")
    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list"], [
            ["normal", ["a", "b"], [[10, 11], [20, 21]]],
            ["normal", None, [[10, 11], [20, 21]]],
        ]
    )
    def test_normal(self, table_name, header_list, record_list):
        import pandas

        tabledata = TableData(table_name, header_list, record_list)

        dataframe = pandas.DataFrame(record_list)
        if dp.is_not_empty_sequence(header_list):
            dataframe.columns = header_list

        print("lhs: {}".format(tabledata.as_dataframe()))
        print("rhs: {}".format(dataframe))

        assert tabledata.as_dataframe().equals(dataframe)


class Test_TableData_hash:

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list"], [
            ["tablename", ["a", "b"], []],
        ]
    )
    def test_normal(self, table_name, header_list, record_list):
        tabledata_a0 = TableData(table_name, header_list, record_list)
        tabledata_a1 = TableData(table_name, header_list, record_list)
        tabledata_b0 = TableData("dummy", header_list, record_list)

        assert tabledata_a0.__hash__() == tabledata_a1.__hash__()
        assert tabledata_a0.__hash__() != tabledata_b0.__hash__()


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
