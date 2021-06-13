"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
from decimal import Decimal

import pytest
from path import Path
from pytablewriter import dumps_tabledata
from simplesqlite import SimpleSQLite
from tabledata import TableData

import pytablereader as ptr
from pytablereader.interface import AbstractTableReader


Data = collections.namedtuple("Data", "value expected")

test_data_00 = Data(
    TableData(
        "tmp",
        ["attr_a", "attr_b", "attr_c"],
        [[1, 4, "a"], [2, Decimal("2.1"), "bb"], [3, Decimal("120.9"), "ccc"]],
    ),
    [
        TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [[1, 4, "a"], [2, Decimal("2.1"), "bb"], [3, Decimal("120.9"), "ccc"]],
        )
    ],
)
test_data_01 = Data(
    TableData(
        "foo_bar",
        ["attr_a", "attr_b", "attr_c"],
        [["aaaa", "bbbb", "cccc"], [1, 4, "a"], [2, "2.1", "bb"], [3, "120.9", "ccc"]],
    ),
    [
        TableData(
            "foo_bar",
            ["attr_a", "attr_b", "attr_c"],
            [["aaaa", "bbbb", "cccc"], ["1", "4", "a"], ["2", "2.1", "bb"], ["3", "120.9", "ccc"]],
        )
    ],
)
test_data_02 = Data(
    TableData("foo_bar", ["attr_a", "attr_b", "attr_c"], [[3, "120.9", "ccc"]]),
    [TableData("foo_bar", ["attr_a", "attr_b", "attr_c"], [[3, "120.9", "ccc"]])],
)
test_data_03 = Data(
    TableData(
        "tmp", ["attr_a", "attr_b", "attr_c"], [[1, 4, "a"], [2, "2.1", "bb"], [3, "120.9", "ccc"]]
    ),
    [
        TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [[1, 4, "a"], [2, "2.1", "bb"], [3, "120.9", "ccc"]],
        )
    ],
)
test_data_04 = Data(
    TableData(
        "tmp", ["attr_a", "attr_b", "attr_c"], [[1, 4, "a"], [2, "2.1", "bb"], [3, "120.9", "ccc"]]
    ),
    [
        TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [[1, 4, "a"], [2, "2.1", "bb"], [3, "120.9", "ccc"]],
        )
    ],
)
test_data_05 = Data(
    TableData(
        "tmp",
        ["姓", "名", "生年月日", "郵便番号", "住所", "電話番号"],
        [
            ["山田", "太郎", "2001/1/1", "100-0002", "東京都千代田区皇居外苑", "03-1234-5678"],
            ["山田", "次郎", "2001/1/2", "251-0036", "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
        ],
    ),
    [
        TableData(
            "tmp",
            ["姓", "名", "生年月日", "郵便番号", "住所", "電話番号"],
            [
                ["山田", "太郎", "2001/1/1", "100-0002", "東京都千代田区皇居外苑", "03-1234-5678"],
                ["山田", "次郎", "2001/1/2", "251-0036", "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
            ],
        )
    ],
)


class Test_SqliteFileLoader_load:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["test_id", "tabledata", "filename", "headers", "expected"],
        [
            [0, test_data_00.value, "tmp.sqlite", [], test_data_00.expected],
            [
                1,
                test_data_01.value,
                "foo_bar.sqlite",
                ["attr_a", "attr_b", "attr_c"],
                test_data_01.expected,
            ],
            [
                2,
                test_data_02.value,
                "foo_bar.sqlite",
                ["attr_a", "attr_b", "attr_c"],
                test_data_02.expected,
            ],
            [3, test_data_03.value, "tmp.sqlite", [], test_data_03.expected],
            [4, test_data_04.value, "tmp.sqlite", [], test_data_04.expected],
            [5, test_data_05.value, "tmp.sqlite", [], test_data_05.expected],
        ],
    )
    def test_normal(self, tmpdir, test_id, tabledata, filename, headers, expected):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        con = SimpleSQLite(file_path, "w")

        con.create_table_from_tabledata(tabledata)

        loader = ptr.SqliteFileLoader(file_path)
        loader.headers = headers

        for tabledata in loader.load():
            print(f"test-id={test_id}")
            print(dumps_tabledata(tabledata))

            assert tabledata.in_tabledata_list(expected)

    @pytest.mark.parametrize(
        ["filename", "headers", "expected"],
        [["", [], ptr.InvalidFilePathError], [None, [], ptr.InvalidFilePathError]],
    )
    def test_null(self, tmpdir, filename, headers, expected):
        loader = ptr.SqliteFileLoader(filename)
        loader.headers = headers

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
