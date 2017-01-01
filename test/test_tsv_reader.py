# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function
from __future__ import unicode_literals
import collections
import io

from path import Path
import pytablewriter as ptw
import pytest

import pytablereader as ptr
from pytablereader.interface import TableLoader
from pytablereader import TableData
from pytablereader import InvalidTableNameError


Data = collections.namedtuple("Data", "value expected")

test_data_00 = Data(
    "\n".join([
        '"attr_a"\t"attr_b"\t"attr_c"',
        '1\t4\t"a"',
        '2\t2.1\t"bb"',
        '3\t120.9\t"ccc"',
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

test_data_01 = Data(
    "\n".join([
        '"attr_a"\t"attr_b"\t"attr_c"',
        '1\t4\t"a"',
        '2\t2.1\t"bb"',
        '3\t120.9\t"ccc"',
    ]),
    [
        TableData(
            "foo_bar",
            ["attr_a", "attr_b", "attr_c"],
            [
                ["attr_a", "attr_b", "attr_c"],
                [1, 4,      "a"],
                [2, "2.1",    "bb"],
                [3, "120.9",  "ccc"],
            ]),
    ])

test_data_02 = Data(
    "\n".join([
        '3\t120.9\t"ccc"',
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
        '"attr_a"\t"attr_b"\t"attr_c"',
        '1\t4\t"a"',
        '2\t2.1\t"bb"',
        '3\t120.9\t"ccc"',
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


class Test_TsvTableFileLoader_make_table_name:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(["value", "source", "expected"], [
        ["%(default)s", "/path/to/data.tsv", "data"],
        ["%(filename)s", "/path/to/data.tsv", "data"],
        ["prefix_%(filename)s", "/path/to/data.tsv", "prefix_data"],
        ["%(filename)s_suffix", "/path/to/data.tsv", "data_suffix"],
        [
            "prefix_%(filename)s_suffix",
            "/path/to/data.tsv",
            "prefix_data_suffix"
        ],
        [
            "%(filename)s%(filename)s",
            "/path/to/data.tsv",
            "datadata"
        ],
        [
            "%(format_name)s%(format_id)s_%(filename)s",
            "/path/to/data.tsv",
            "tsv0_data",
        ],
        [
            "%(%(filename)s)",
            "/path/to/data.tsv",
            "%(data)"
        ],
    ])
    def test_normal(self, value, source, expected):
        loader = ptr.TsvTableFileLoader(source)
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "/path/to/data.tsv", ValueError],
        ["", "/path/to/data.tsv", ValueError],
        ["%(filename)s", None, InvalidTableNameError],
        ["%(filename)s", "", InvalidTableNameError],
    ])
    def test_exception(self, value, source, expected):
        loader = ptr.TsvTableFileLoader(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_TsvTableFileLoader_load:

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
                "tmp.tsv",
                [],
                test_data_00.expected,
            ],
            [
                1, test_data_01.value,
                "hoge/foo_bar.tsv",
                ["attr_a", "attr_b", "attr_c"],
                test_data_01.expected,
            ],
            [
                2, test_data_02.value,
                "hoge/foo_bar.tsv",
                ["attr_a", "attr_b", "attr_c"],
                test_data_02.expected,
            ],
            [
                3, test_data_03.value,
                "tmp.tsv",
                [],
                test_data_03.expected,
            ],
        ])
    def test_normal(
            self, tmpdir,
            test_id, table_text, filename, header_list, expected):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        with io.open(file_path, "w", encoding="utf-8") as f:
            f.write(table_text)

        loader = ptr.TsvTableFileLoader(file_path)
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
                "hoge.tsv",
                [],
                ptr.InvalidDataError,
            ],
            [
                "\n".join([
                    '"attr_a"\t"attr_b"\t"attr_c"',
                ]),
                "hoge.tsv",
                [],
                ptr.InvalidDataError,
            ],
            [
                "\n".join([
                ]),
                "hoge.tsv",
                ["attr_a", "attr_b", "attr_c"],
                ptr.InvalidDataError,
            ],
        ])
    def test_exception(
            self, tmpdir, table_text, filename, header_list, expected):
        p_tsv = tmpdir.join(filename)

        with io.open(str(p_tsv), "w", encoding="utf8") as f:
            f.write(table_text)

        loader = ptr.TsvTableFileLoader(str(p_tsv))
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
            ["", [], IOError],
            [None, [], IOError],
        ])
    def test_null(
            self, tmpdir, filename, header_list, expected):

        loader = ptr.TsvTableFileLoader(filename)
        loader.header_list = header_list

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


class Test_TsvTableTextLoader_make_table_name:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(["value", "expected"], [
        ["%(format_name)s%(format_id)s", "tsv0"],
        ["tablename", "tablename"],
    ])
    def test_normal(self, value, expected):
        loader = ptr.TsvTableTextLoader("dummy")
        loader.table_name = value

        assert loader.make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "tablename", ValueError],
        ["", "tablename", ValueError],
    ])
    def test_exception(self, value, source, expected):
        loader = ptr.TsvTableFileLoader(source)
        loader.table_name = value

        with pytest.raises(expected):
            loader.make_table_name()


class Test_TsvTableTextLoader_load:

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
        loader = ptr.TsvTableTextLoader(table_text)
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
                    '"attr_a"\t"attr_b"\t"attr_c"',
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
        loader = ptr.TsvTableTextLoader(table_text)
        loader.table_name = table_name
        loader.header_list = header_list

        with pytest.raises(expected):
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
        loader = ptr.TsvTableTextLoader("dummy")
        loader.table_name = table_name
        loader.header_list = header_list

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
