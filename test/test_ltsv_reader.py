# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function
from __future__ import unicode_literals
import collections
from decimal import Decimal
import io

from path import Path
import pytablewriter as ptw
import pytest

import pytablereader as ptr
from pytablereader.interface import TableLoader
from pytablereader import TableData
from pytablereader import (
    InvalidTableNameError,
    InvalidDataError,
    InvalidHeaderNameError
)


Data = collections.namedtuple("Data", "value expected")

test_data_00 = Data(
    """a.0:1\tb-1:123.1\tc_2:"a"\t"dd":1.0\te.f-g_4:"1"
a.0:2\tb-1:2.2\tc_2:"bb"\t"dd":2.2\te.f-g_4:"2.2"
a.0:3\tb-1:3.3\tc_2:"ccc"\t"dd":3.0\te.f-g_4:"cccc"
""",
    TableData(
        "tmp",
        ["a.0", "b-1", "c_2", "dd", "e.f-g_4"],
        [
            [1, Decimal("123.1"), "a", 1, 1],
            [2, Decimal("2.2"), "bb", Decimal("2.2"), Decimal("2.2")],
            [3, Decimal("3.3"), "ccc", 3, "cccc"],
        ])
)


class Test_LtsvTableFileLoader_make_table_name:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(["value", "source", "expected"], [
        ["%(default)s", "/path/to/data.ltsv", "data"],
        ["%(filename)s", "/path/to/data.ltsv", "data"],
        ["prefix_%(filename)s", "/path/to/data.ltsv", "prefix_data"],
        ["%(filename)s_suffix", "/path/to/data.ltsv", "data_suffix"],
        [
            "prefix_%(filename)s_suffix",
            "/path/to/data.ltsv",
            "prefix_data_suffix"
        ],
        [
            "%(filename)s%(filename)s",
            "/path/to/data.ltsv",
            "datadata"
        ],
        [
            "%(format_name)s%(format_id)s_%(filename)s",
            "/path/to/data.ltsv",
            "ltsv0_data",
        ],
        [
            "%(%(filename)s)",
            "/path/to/data.ltsv",
            "%(data)"
        ],
    ])
    def test_normal(self, value, source, expected):
        loader = ptr.LtsvTableFileLoader(source)
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "/path/to/data.ltsv", ValueError],
        ["", "/path/to/data.ltsv", ValueError],
        ["%(filename)s", None, InvalidTableNameError],
        ["%(filename)s", "", InvalidTableNameError],
    ])
    def test_exception(self, value, source, expected):
        loader = ptr.LtsvTableFileLoader(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_LtsvTableFileLoader_load:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        [
            "test_id",
            "table_text",
            "filename",
            "expected",
        ],
        [
            [
                0, test_data_00.value,
                "tmp.ltsv",
                test_data_00.expected,
            ],
        ])
    def test_normal(
            self, tmpdir, test_id, table_text, filename, expected):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        with io.open(file_path, "w", encoding="utf-8") as f:
            f.write(table_text)

        loader = ptr.LtsvTableFileLoader(file_path)

        for tabledata in loader.load():
            print("test-id={}".format(test_id))
            print("[expected]: {}".format(ptw.dump_tabledata(expected)))
            print("[actual]: {}".format(ptw.dump_tabledata(tabledata)))

            assert tabledata == expected

    @pytest.mark.parametrize(["table_text", "filename", "expected"], [
        [
            "\n".join([
                '"attr_a"\t"attr_b"\t"attr_c"',
            ]),
            "hoge.ltsv",
            ptr.InvalidDataError,
        ],
        [
            "\n".join([
                '"a":1"\t"attr_b"\t"attr_c"',
            ]),
            "hoge.ltsv",
            ptr.InvalidDataError,
        ],
    ])
    def test_exception(self, tmpdir, table_text, filename, expected):
        p_ltsv = tmpdir.join(filename)

        with io.open(str(p_ltsv), "w", encoding="utf8") as f:
            f.write(table_text)

        loader = ptr.LtsvTableFileLoader(str(p_ltsv))

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
            ["", [], IOError],
            [None, [], IOError],
        ])
    def test_null(
            self, tmpdir, filename, header_list, expected):

        loader = ptr.LtsvTableFileLoader(filename)
        loader.header_list = header_list

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


class Test_LtsvTableTextLoader_make_table_name:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(["value", "expected"], [
        ["%(format_name)s%(format_id)s", "ltsv0"],
        ["tablename", "tablename"],
    ])
    def test_normal(self, value, expected):
        loader = ptr.LtsvTableTextLoader("dummy")
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "tablename", ValueError],
        ["", "tablename", ValueError],
    ])
    def test_exception(self, value, source, expected):
        loader = ptr.LtsvTableFileLoader(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_LtsvTableTextLoader_load:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(["table_text", "table_name", "expected"], [
        [
            test_data_00.value,
            "tmp",
            test_data_00.expected,
        ],
    ])
    def test_normal(self, table_text, table_name, expected):
        loader = ptr.LtsvTableTextLoader(table_text)
        loader.table_name = table_name

        for tabledata in loader.load():
            print("[expected]: {}".format(ptw.dump_tabledata(expected)))
            print("[actual]: {}".format(ptw.dump_tabledata(tabledata)))

            assert tabledata == expected

    @pytest.mark.parametrize(["table_text", "table_name", "expected"], [
        [
            '"":"invalid"\ta:1',
            "dummy",
            InvalidHeaderNameError,
        ],
        [
            "",
            "dummy",
            InvalidDataError,
        ],
        [
            'a!:1\tb:2',
            "dummy",
            InvalidHeaderNameError,
        ],
        [
            'a:1\tb$c:2',
            "dummy",
            InvalidHeaderNameError,
        ],
    ])
    def test_exception_insufficient_data(
            self, table_text, table_name, expected):
        loader = ptr.LtsvTableTextLoader(table_text)
        loader.table_name = table_name

        with pytest.raises(expected):
            for _tabledata in loader.load():
                print(_tabledata)
                pass

    @pytest.mark.parametrize(["table_name", "expected"], [
        ["", ValueError],
        [None, ValueError],
    ])
    def test_null(self, table_name, expected):
        loader = ptr.LtsvTableTextLoader("dummy")
        loader.table_name = table_name

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
