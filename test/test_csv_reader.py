"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import os
import platform
import sys  # noqa
from concurrent.futures import ProcessPoolExecutor
from decimal import Decimal
from textwrap import dedent

import pytest
from path import Path
from pytablewriter import dumps_tabledata
from tabledata import TableData
from typepy import Integer, RealNumber, String

import pytablereader as ptr
from pytablereader import InvalidTableNameError
from pytablereader.interface import AbstractTableReader

from ._common import TYPE_HINT_RULES, fifo_writer


Data = collections.namedtuple("Data", "value expected")

test_data_00 = Data(
    "\n".join(
        [
            '"attr_a","attr_b","attr_c"',
            '1,4,"a"',
            '2,2.1,"bb"',
            '3,120.9,"ccc"',
        ]
    ),
    [
        TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [
                [1, 4, "a"],
                [2, Decimal("2.1"), "bb"],
                [3, Decimal("120.9"), "ccc"],
            ],
        )
    ],
)
test_data_01 = Data(
    "\n".join(
        [
            '"attr_a","attr_b","attr_c"',
            ' 1,4,"a"',
            '2, 2.1,"bb"',
            '3,120.9, "ccc"',
        ]
    ),
    [
        TableData(
            "foo_bar",
            ["attr_a", "attr_b", "attr_c"],
            [
                ["attr_a", "attr_b", "attr_c"],
                [1, 4, "a"],
                [2, Decimal("2.1"), "bb"],
                [3, Decimal("120.9"), "ccc"],
            ],
        )
    ],
)
test_data_02 = Data(
    "\n".join(['3,120.9,"ccc"']),
    [TableData("foo_bar", ["attr_a", "attr_b", "attr_c"], [[3, "120.9", "ccc"]])],
)
test_data_03 = Data(
    "\n".join(['"attr_a","attr_b","attr_c"', '1,4,"a"', '2,2.1,"bb"', '3,120.9,"ccc"', "", ""]),
    [
        TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [[1, 4, "a"], [2, Decimal("2.1"), "bb"], [3, Decimal("120.9"), "ccc"]],
        )
    ],
)
test_data_04 = Data(
    dedent(
        """\
        "attr_a","attr_b","attr_c"
        1,4,"a"
        2,2.1,"bb"
        3,120.9,"ccc"

        """
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
    dedent(
        """\
        "姓","名","生年月日","郵便番号","住所","電話番号"
        "山田","太郎","2001/1/1","100-0002","東京都千代田区皇居外苑","03-1234-5678"
        "山田","次郎","2001/1/2","251-0036","神奈川県藤沢市江の島１丁目","03-9999-9999"
        """
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

test_data_06 = Data(
    dedent(
        """\
        smokey,Linux 3.0-ARCH,x86
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
        """
    ),
    [
        TableData(
            "tmp",
            ["smokey", "Linux 3.0-ARCH", "x86"],
            [
                ["12345678901", "12345 1234567890123", "123"],
                ["12345678901", "1234567890123456789", "12345"],
                ["11 bytes", "19 bytes", "5 byt"],
                ["test line:", 'Some "comma, quote"', "foo"],
                ["skylight", "Linux 3.0-ARCH", "x86"],
                ["polaris", "Linux 3.0-ARCH", "amd64"],
                ["asgard", "Windows 6.1.7600", "amd64"],
                ["galileo", "Windows 6.2.8102", "x86"],
                ["kepler", "Windows 6.2.8123", "amd64"],
                ["wrfbox", "Windows 6.2.8133", "amd64"],
            ],
        )
    ],
)
test_data_multibyte = Data(
    dedent(
        """\
        "姓","名","生年月日","郵便番号","住所","電話番号"
        "山田","太郎","2001/1/1","100-0002","東京都千代田区皇居外苑","03-1234-5678"
        "山田","次郎","2001/1/2","251-0036","神奈川県藤沢市江の島１丁目","03-9999-9999"
        """
    ),
    [
        TableData(
            "multibyte",
            ["姓", "名", "生年月日", "郵便番号", "住所", "電話番号"],
            [
                ["山田", "太郎", "2001/1/1", "100-0002", "東京都千代田区皇居外苑", "03-1234-5678"],
                ["山田", "次郎", "2001/1/2", "251-0036", "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
            ],
        )
    ],
)


class Test_CsvTableFileLoader_make_table_name:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(default)s", "/path/to/data.csv", "data"],
            ["%(filename)s", "/path/to/data.csv", "data"],
            ["prefix_%(filename)s", "/path/to/data.csv", "prefix_data"],
            ["%(filename)s_suffix", "/path/to/data.csv", "data_suffix"],
            ["prefix_%(filename)s_suffix", "/path/to/data.csv", "prefix_data_suffix"],
            ["%(filename)s%(filename)s", "/path/to/data.csv", "datadata"],
            ["%(format_name)s%(format_id)s_%(filename)s", "/path/to/data.csv", "csv0_data"],
            ["%(%(filename)s)", "/path/to/data.csv", "%(data)"],
        ],
    )
    def test_normal(self, value, source, expected):
        loader = ptr.CsvTableFileLoader(source)
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            [None, "/path/to/data.csv", ValueError],
            ["", "/path/to/data.csv", ValueError],
            ["%(filename)s", None, InvalidTableNameError],
            ["%(filename)s", "", InvalidTableNameError],
        ],
    )
    def test_exception(self, value, source, expected):
        loader = ptr.CsvTableFileLoader(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_CsvTableFileLoader_load:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["test_id", "table_text", "filename", "headers", "type_hints", "expected"],
        [
            [0, test_data_00.value, "tmp.csv", [], [], test_data_00.expected],
            [
                1,
                test_data_01.value,
                "hoge/foo_bar.csv",
                ["attr_a", "attr_b", "attr_c"],
                [Integer, RealNumber, String],
                test_data_01.expected,
            ],
            [
                2,
                test_data_02.value,
                "hoge/foo_bar.csv",
                ["attr_a", "attr_b", "attr_c"],
                [Integer, RealNumber, String],
                test_data_02.expected,
            ],
            [3, test_data_03.value, "tmp.csv", [], [], test_data_03.expected],
            [4, test_data_04.value, "tmp.csv", [], [], test_data_04.expected],
            [5, test_data_05.value, "tmp.csv", [], [], test_data_05.expected],
            [6, test_data_06.value, "tmp.csv", [], [], test_data_06.expected],
        ],
    )
    def test_normal(self, tmpdir, test_id, table_text, filename, headers, type_hints, expected):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(table_text)

        loader = ptr.CsvTableFileLoader(file_path, type_hints=type_hints)
        loader.headers = headers

        for tabledata in loader.load():
            print(f"test-id={test_id}")
            print(dumps_tabledata(tabledata))

            assert tabledata.in_tabledata_list(expected)

    @pytest.mark.parametrize(
        ["test_id", "table_text", "filename", "encoding", "headers", "expected"],
        [
            [
                7,
                test_data_multibyte.value,
                "multibyte.csv",
                "utf16",
                [],
                test_data_multibyte.expected,
            ]
        ],
    )
    def test_normal_multibyte(
        self, tmpdir, test_id, table_text, filename, encoding, headers, expected
    ):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        with open(file_path, "w", encoding=encoding) as f:
            f.write(table_text)

        loader = ptr.CsvTableFileLoader(file_path)
        loader.headers = headers

        for tabledata in loader.load():
            print(f"test-id={test_id}")
            print(dumps_tabledata(tabledata))

            assert tabledata.in_tabledata_list(expected)

    @pytest.mark.skipif(platform.system() == "Windows", reason="platform dependent tests")
    @pytest.mark.parametrize(
        ["table_text", "fifo_name", "expected"],
        [[test_data_06.value, "tmp", test_data_06.expected]],
    )
    def test_normal_fifo(self, tmpdir, table_text, fifo_name, expected):
        namedpipe = str(tmpdir.join(fifo_name))

        os.mkfifo(namedpipe)

        loader = ptr.CsvTableFileLoader(namedpipe)

        with ProcessPoolExecutor() as executor:
            executor.submit(fifo_writer, namedpipe, table_text)

            for tabledata in loader.load():
                print(dumps_tabledata(tabledata))

                assert tabledata.in_tabledata_list(expected)

    @pytest.mark.parametrize(
        ["table_text", "filename", "headers", "expected"],
        [
            ["", "hoge.csv", [], ptr.DataError],
            ["\n".join(['"attr_a","attr_b","attr_c"']), "hoge.csv", [], ptr.DataError],
            ["\n".join([]), "hoge.csv", ["attr_a", "attr_b", "attr_c"], ptr.DataError],
        ],
    )
    def test_exception(self, tmpdir, table_text, filename, headers, expected):
        p_csv = tmpdir.join(filename)

        with open(str(p_csv), "w", encoding="utf8") as f:
            f.write(table_text)

        loader = ptr.CsvTableFileLoader(str(p_csv))
        loader.headers = headers

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(
        ["filename", "headers", "expected"],
        [["", [], ptr.InvalidFilePathError], [None, [], ptr.InvalidFilePathError]],
    )
    def test_null(self, tmpdir, filename, headers, expected):
        loader = ptr.CsvTableFileLoader(filename)
        loader.headers = headers

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


class Test_CsvTableTextLoader_make_table_name:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["value", "expected"],
        [["%(format_name)s%(format_id)s", "csv0"], ["tablename", "tablename"]],
    )
    def test_normal(self, value, expected):
        loader = ptr.CsvTableTextLoader("dummy")
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [[None, "tablename", ValueError], ["", "tablename", ValueError]],
    )
    def test_exception(self, value, source, expected):
        loader = ptr.CsvTableFileLoader(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_CsvTableTextLoader_load:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @pytest.mark.parametrize(
        ["table_text", "table_name", "headers", "type_hints", "expected"],
        [
            [test_data_00.value, "tmp", [], [], test_data_00.expected],
            [
                test_data_01.value,
                "foo_bar",
                ["attr_a", "attr_b", "attr_c"],
                [Integer, RealNumber, String],
                test_data_01.expected,
            ],
            [
                test_data_02.value,
                "foo_bar",
                ["attr_a", "attr_b", "attr_c"],
                [Integer, RealNumber, String],
                test_data_02.expected,
            ],
            [test_data_03.value, "tmp", [], [], test_data_03.expected],
        ],
    )
    def test_normal(self, table_text, table_name, headers, type_hints, expected):
        loader = ptr.CsvTableTextLoader(table_text, type_hints=type_hints)
        loader.table_name = table_name
        loader.headers = headers

        for tabledata in loader.load():
            print(dumps_tabledata(tabledata))
            for e in expected:
                print(dumps_tabledata(e))

            assert tabledata.in_tabledata_list(expected)

    def test_normal_type_hint_rules(self):
        table_text = dedent(
            """\
            "a text","b integer","c real"
            01,"01","1.1"
            20,"20","1.2"
            030,"030","1.3"
            """
        )

        loader = ptr.CsvTableTextLoader(table_text)
        loader.table_name = "type hint rules"
        loader.type_hint_rules = TYPE_HINT_RULES

        for tbldata in loader.load():
            assert tbldata.headers == ["a text", "b integer", "c real"]
            assert tbldata.value_matrix == [
                ["01", 1, Decimal("1.1")],
                ["20", 20, Decimal("1.2")],
                ["030", 30, Decimal("1.3")],
            ]

    @pytest.mark.parametrize(
        ["table_text", "table_name", "headers", "expected"],
        [
            ["", "hoge", [], ValueError],
            ["\n".join(['"attr_a","attr_b","attr_c"']), "hoge", [], ptr.DataError],
            ["\n".join([]), "hoge", ["attr_a", "attr_b", "attr_c"], ValueError],
        ],
    )
    def test_exception_insufficient_data(self, table_text, table_name, headers, expected):
        loader = ptr.CsvTableTextLoader(table_text)
        loader.table_name = table_name
        loader.headers = headers

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    def test_exception_invalid_csv(self):
        table_text = dedent(
            """\
            nan = float("nan")
            inf = float("inf")
            TEST_TABLE_NAME = "test_table"
            TEST_DB_NAME = "test_db"
            NOT_EXIT_FILE_PATH = "/not/existing/file/__path__"

            NamedTuple = namedtuple("NamedTuple", "attr_a attr_b")
            NamedTupleEx = namedtuple("NamedTupleEx", "attr_a attr_b attr_c")
            """
        )
        loader = ptr.CsvTableTextLoader(table_text)
        loader.table_name = "dummy"

        with pytest.raises(ptr.DataError):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(
        ["table_name", "headers", "expected"], [["", [], ValueError], [None, [], ValueError]]
    )
    def test_null(self, table_name, headers, expected):
        loader = ptr.CsvTableTextLoader("dummy")
        loader.table_name = table_name
        loader.headers = headers

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
