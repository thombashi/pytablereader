"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import pytest
from pytablewriter import dumps_tabledata
from tabledata import TableData

import pytablereader as ptr
from pytablereader.interface import AbstractTableReader


class Test_TableTextLoader_get_format_names:
    def test_normal(self):
        assert ptr.TableTextLoader.get_format_names() == [
            "csv",
            "html",
            "json",
            "json_lines",
            "jsonl",
            "ldjson",
            "ltsv",
            "markdown",
            "mediawiki",
            "ndjson",
            "ssv",
            "tsv",
        ]


class Test_TableTextLoader_constructor:
    @pytest.mark.parametrize(
        ["value", "format_name", "expected"],
        [
            [None, None, ValueError],
            ["", None, ValueError],
            ["https://github.com/", None, ValueError],
            ["/tmp/valid/test/data/validext.csv/", None, ValueError],
            ["/tmp/invalid/test/data/invalidext.txt", "invalidformat", ptr.LoaderNotFoundError],
        ],
    )
    def test_exception(self, value, format_name, expected):
        with pytest.raises(expected):
            ptr.TableTextLoader(value, format_name=format_name)


class Test_TableTextLoader_load:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    def test_normal_csv(self):
        text = dedent(
            """\
            "attr_a","attr_b","attr_c"
            1,4,"a"
            2,2.1,"bb"
            3,120.9,"ccc"
            """
        )

        expected_list = [
            TableData(
                "csv1",
                ["attr_a", "attr_b", "attr_c"],
                [[1, 4, "a"], [2, "2.1", "bb"], [3, "120.9", "ccc"]],
            )
        ]
        loader = ptr.TableTextLoader(text, format_name="csv")

        assert loader.format_name == "csv"

        for tabledata, expected in zip(loader.load(), expected_list):
            print(dumps_tabledata(expected))
            print(dumps_tabledata(tabledata))

            assert tabledata.equals(expected)

    def test_normal_ssv(self):
        text = dedent(
            """\
            USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
            root         1  0.0  0.4  77664  8784 ?        Ss   May11   0:02 /sbin/init
            root         2  0.0  0.0      0     0 ?        S    May11   0:00 [kthreadd]
            root         4  0.0  0.0      0     0 ?        I<   May11   0:00 [kworker/0:0H]
            root         6  0.0  0.0      0     0 ?        I<   May11   0:00 [mm_percpu_wq]
            root         7  0.0  0.0      0     0 ?        S    May11   0:01 [ksoftirqd/0]
            """
        )

        expected_list = [
            TableData(
                "csv1",
                [
                    "USER",
                    "PID",
                    "%CPU",
                    "%MEM",
                    "VSZ",
                    "RSS",
                    "TTY",
                    "STAT",
                    "START",
                    "TIME",
                    "COMMAND",
                ],
                [
                    ["root", 1, 0, 0.4, 77664, 8784, "?", "Ss", "May11", "0:02", "/sbin/init"],
                    ["root", 2, 0, 0, 0, 0, "?", "S", "May11", "0:00", "[kthreadd]"],
                    ["root", 4, 0, 0, 0, 0, "?", "I<", "May11", "0:00", "[kworker/0:0H]"],
                    ["root", 6, 0, 0, 0, 0, "?", "I<", "May11", "0:00", "[mm_percpu_wq]"],
                    ["root", 7, 0, 0, 0, 0, "?", "S", "May11", "0:01", "[ksoftirqd/0]"],
                ],
            )
        ]
        loader = ptr.TableTextLoader(text, format_name="ssv")

        assert loader.format_name == "csv"

        for tabledata, expected in zip(loader.load(), expected_list):
            print(dumps_tabledata(expected))
            print(dumps_tabledata(tabledata))

            assert tabledata.equals(expected)

    def test_normal_json(self):
        text = dedent(
            """\
            [
                {"attr_a": 1},
                {"attr_b": 2.1, "attr_c": "bb"}
            ]"""
        )

        expected_list = [
            TableData(
                "json1",
                ["attr_a", "attr_b", "attr_c"],
                [{"attr_a": 1}, {"attr_b": 2.1, "attr_c": "bb"}],
            )
        ]
        loader = ptr.TableTextLoader(text, format_name="json")

        assert loader.format_name == "json"

        for table_data, expected in zip(loader.load(), expected_list):
            print(dumps_tabledata(expected))
            print(dumps_tabledata(table_data))

            assert table_data.equals(expected)
