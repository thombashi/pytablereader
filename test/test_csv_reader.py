# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function
from __future__ import unicode_literals

import collections
from decimal import Decimal
import io

from path import Path
from pytablereader import InvalidTableNameError
from pytablereader import TableData
from pytablereader.interface import TableLoader
import pytest

import pytablereader as ptr
import pytablewriter as ptw


Data = collections.namedtuple("Data", "value expected")

test_data_00 = Data(
    "\n".join([
        '"attr_a","attr_b","attr_c"',
        '1,4,"a"',
        '2,2.1,"bb"',
        '3,120.9,"ccc"',
    ]),
    [
        TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [
                [1, 4, "a"],
                [2, Decimal("2.1"), "bb"],
                [3, Decimal("120.9"), "ccc"],
            ])
    ])

test_data_01 = Data(
    "\n".join([
        '"attr_a","attr_b","attr_c"',
        ' 1,4,"a"',
        '2, 2.1,"bb"',
        '3,120.9, "ccc"',
    ]),
    [
        TableData(
            "foo_bar",
            ["attr_a", "attr_b", "attr_c"],
            [
                ["attr_a", "attr_b", "attr_c"],
                [1, 4, "a"],
                [2, "2.1",    "bb"],
                [3, "120.9",  "ccc"],
            ]),
    ])

test_data_02 = Data(
    "\n".join([
        '3,120.9,"ccc"',
    ]),
    [
        TableData(
            "foo_bar",
            ["attr_a", "attr_b", "attr_c"],
            [
                [3, "120.9",  "ccc"],
            ]),
    ])

test_data_03 = Data(
    "\n".join([
        '"attr_a","attr_b","attr_c"',
        '1,4,"a"',
        '2,2.1,"bb"',
        '3,120.9,"ccc"',
        "",
        "",
    ]),
    [
        TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [
                [1, 4,      "a"],
                [2, "2.1",    "bb"],
                [3, "120.9",  "ccc"],
            ])
    ])

test_data_04 = Data(
    """"attr_a","attr_b","attr_c"
1,4,"a"
2,2.1,"bb"
3,120.9,"ccc"

""",
    [
        TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [
                [1, 4, "a"],
                [2, "2.1", "bb"],
                [3, "120.9", "ccc"],
            ])
    ])

test_data_05 = Data(
    """"姓","名","生年月日","郵便番号","住所","電話番号"
"山田","太郎","2001/1/1","100-0002","東京都千代田区皇居外苑","03-1234-5678"
"山田","次郎","2001/1/2","251-0036","神奈川県藤沢市江の島１丁目","03-9999-9999"
""",
    [
        TableData(
            "tmp",
            ["姓", "名", "生年月日", "郵便番号", "住所", "電話番号"],
            [
                ["山田", "太郎", "2001/1/1", "100-0002",
                    "東京都千代田区皇居外苑", "03-1234-5678"],
                ["山田", "次郎", "2001/1/2", "251-0036",
                    "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
            ])
    ])

test_data_06 = Data(
    """smokey,Linux 3.0-ARCH,x86
12345678901,12345 1234567890123,123
12345678901,1234567890123456789,12345
11 bytes,19 bytes,5 byt
test line:,"Some \"\"comma, quote\"\"",foo
skylight,Linux 3.0-ARCH,x86
polaris,Linux 3.0-ARCH,amd64
asgard,Windows 6.1.7600,amd64
galileo,Windows 6.2.8102,x86
kepler,Windows 6.2.8123,amd64
wrfbox,Windows 6.2.8133,amd64
""",
    [
        TableData(
            "tmp",
            ["smokey", "Linux 3.0-ARCH", "x86"],
            [
                [12345678901, "12345 1234567890123", 123],
                [12345678901, 1234567890123456789, 12345],
                ["11 bytes", "19 bytes", "5 byt"],
                ["test line:", 'Some "comma, quote"', "foo"],
                ["skylight", "Linux 3.0-ARCH", "x86"],
                ["polaris", "Linux 3.0-ARCH", "amd64"],
                ["asgard", "Windows 6.1.7600", "amd64"],
                ["galileo", "Windows 6.2.8102", "x86"],
                ["kepler", "Windows 6.2.8123", "amd64"],
                ["wrfbox", "Windows 6.2.8133", "amd64"],
            ])
    ])


class Test_CsvTableFileLoader_make_table_name(object):

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(["value", "source", "expected"], [
        ["%(default)s", "/path/to/data.csv", "data"],
        ["%(filename)s", "/path/to/data.csv", "data"],
        ["prefix_%(filename)s", "/path/to/data.csv", "prefix_data"],
        ["%(filename)s_suffix", "/path/to/data.csv", "data_suffix"],
        [
            "prefix_%(filename)s_suffix",
            "/path/to/data.csv",
            "prefix_data_suffix"
        ],
        [
            "%(filename)s%(filename)s",
            "/path/to/data.csv",
            "datadata"
        ],
        [
            "%(format_name)s%(format_id)s_%(filename)s",
            "/path/to/data.csv",
            "csv0_data",
        ],
        [
            "%(%(filename)s)",
            "/path/to/data.csv",
            "%(data)"
        ],
    ])
    def test_normal(self, value, source, expected):
        loader = ptr.CsvTableFileLoader(source)
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "/path/to/data.csv", ValueError],
        ["", "/path/to/data.csv", ValueError],
        ["%(filename)s", None, InvalidTableNameError],
        ["%(filename)s", "", InvalidTableNameError],
    ])
    def test_exception(self, value, source, expected):
        loader = ptr.CsvTableFileLoader(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_CsvTableFileLoader_load(object):

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        [
            "test_id",
            "table_text",
            "filename",
            "header_list",
            "expected",
        ],
        [
            [
                0, test_data_00.value,
                "tmp.csv",
                [],
                test_data_00.expected,
            ],
            [
                1, test_data_01.value,
                "hoge/foo_bar.csv",
                ["attr_a", "attr_b", "attr_c"],
                test_data_01.expected,
            ],
            [
                2, test_data_02.value,
                "hoge/foo_bar.csv",
                ["attr_a", "attr_b", "attr_c"],
                test_data_02.expected,
            ],
            [
                3, test_data_03.value,
                "tmp.csv",
                [],
                test_data_03.expected,
            ],
            [
                4, test_data_04.value,
                "tmp.csv",
                [],
                test_data_04.expected,
            ],
            [
                5, test_data_05.value,
                "tmp.csv",
                [],
                test_data_05.expected,
            ],
            [
                6, test_data_06.value,
                "tmp.csv",
                [],
                test_data_06.expected,
            ],
        ])
    def test_normal(
            self, tmpdir,
            test_id, table_text, filename, header_list, expected):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        with io.open(file_path, "w", encoding="utf-8") as f:
            f.write(table_text)

        loader = ptr.CsvTableFileLoader(file_path)
        loader.header_list = header_list

        for tabledata in loader.load():
            print("test-id={}".format(test_id))
            print(ptw.dump_tabledata(tabledata))

            assert tabledata in expected

    @pytest.mark.parametrize(
        [
            "table_text",
            "filename",
            "header_list",
            "expected",
        ],
        [
            [
                "",
                "hoge.csv",
                [],
                ptr.InvalidDataError,
            ],
            [
                "\n".join([
                    '"attr_a","attr_b","attr_c"',
                ]),
                "hoge.csv",
                [],
                ptr.InvalidDataError,
            ],
            [
                "\n".join([
                ]),
                "hoge.csv",
                ["attr_a", "attr_b", "attr_c"],
                ptr.InvalidDataError,
            ],
        ])
    def test_exception(
            self, tmpdir, table_text, filename, header_list, expected):
        p_csv = tmpdir.join(filename)

        with io.open(str(p_csv), "w", encoding="utf8") as f:
            f.write(table_text)

        loader = ptr.CsvTableFileLoader(str(p_csv))
        loader.header_list = header_list

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(
        [
            "filename",
            "header_list",
            "expected",
        ],
        [
            ["", [], ptr.InvalidFilePathError],
            [None, [], ptr.InvalidFilePathError],
        ])
    def test_null(
            self, tmpdir, filename, header_list, expected):

        loader = ptr.CsvTableFileLoader(filename)
        loader.header_list = header_list

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


class Test_CsvTableTextLoader_make_table_name(object):

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(["value", "expected"], [
        ["%(format_name)s%(format_id)s", "csv0"],
        ["tablename", "tablename"],
    ])
    def test_normal(self, value, expected):
        loader = ptr.CsvTableTextLoader("dummy")
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "tablename", ValueError],
        ["", "tablename", ValueError],
    ])
    def test_exception(self, value, source, expected):
        loader = ptr.CsvTableFileLoader(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_CsvTableTextLoader_load(object):

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        [
            "table_text",
            "table_name",
            "header_list",
            "expected",
        ],
        [
            [
                test_data_00.value,
                "tmp",
                [],
                test_data_00.expected,
            ],
            [
                test_data_01.value,
                "foo_bar",
                ["attr_a", "attr_b", "attr_c"],
                test_data_01.expected,
            ],
            [
                test_data_02.value,
                "foo_bar",
                ["attr_a", "attr_b", "attr_c"],
                test_data_02.expected,
            ],
            [
                test_data_03.value,
                "tmp",
                [],
                test_data_03.expected,
            ],
        ])
    def test_normal(self, table_text, table_name, header_list, expected):
        loader = ptr.CsvTableTextLoader(table_text)
        loader.table_name = table_name
        loader.header_list = header_list

        for tabledata in loader.load():
            print(ptw.dump_tabledata(tabledata))
            for e in expected:
                print(ptw.dump_tabledata(e))

            assert tabledata in expected

    @pytest.mark.parametrize(
        [
            "table_text",
            "table_name",
            "header_list",
            "expected",
        ],
        [
            [
                "",
                "hoge",
                [],
                ValueError,
            ],
            [
                "\n".join([
                    '"attr_a","attr_b","attr_c"',
                ]),
                "hoge",
                [],
                ptr.InvalidDataError,
            ],
            [
                "\n".join([
                ]),
                "hoge",
                ["attr_a", "attr_b", "attr_c"],
                ValueError,
            ],
        ])
    def test_exception_insufficient_data(
            self, table_text, table_name, header_list, expected):
        loader = ptr.CsvTableTextLoader(table_text)
        loader.table_name = table_name
        loader.header_list = header_list

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    def test_exception_invalid_csv(self):
        table_text = """nan = float("nan")
inf = float("inf")
TEST_TABLE_NAME = "test_table"
TEST_DB_NAME = "test_db"
NOT_EXIT_FILE_PATH = "/not/existing/file/__path__"

NamedTuple = namedtuple("NamedTuple", "attr_a attr_b")
NamedTupleEx = namedtuple("NamedTupleEx", "attr_a attr_b attr_c")
"""
        loader = ptr.CsvTableTextLoader(table_text)
        loader.table_name = "dummy"

        with pytest.raises(ptr.InvalidDataError):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(
        [
            "table_name",
            "header_list",
            "expected",
        ],
        [
            ["", [], ValueError],
            [None, [], ValueError],
        ])
    def test_null(self, table_name, header_list, expected):
        loader = ptr.CsvTableTextLoader("dummy")
        loader.table_name = table_name
        loader.header_list = header_list

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
