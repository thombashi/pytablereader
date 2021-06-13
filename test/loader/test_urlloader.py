"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os.path
from os.path import dirname
from textwrap import dedent

import pytest
import responses
from pytablewriter import dumps_tabledata
from tabledata import TableData

import pytablereader as ptr
from pytablereader.interface import AbstractTableReader


class Test_TableUrlLoader_get_format_names:
    def test_normal(self):
        assert ptr.TableUrlLoader.get_format_names() == [
            "csv",
            "excel",
            "html",
            "json",
            "json_lines",
            "jsonl",
            "ldjson",
            "ltsv",
            "markdown",
            "mediawiki",
            "ndjson",
            "sqlite",
            "ssv",
            "tsv",
        ]


class Test_TableUrlLoader_constructor:
    @responses.activate
    @pytest.mark.parametrize(
        ["value", "format_name", "expected"],
        [
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.csv",
                None,
                ptr.CsvTableTextLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.csv/",
                None,
                ptr.CsvTableTextLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.xlsx",
                None,
                ptr.ExcelTableFileLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.html",
                None,
                ptr.HtmlTableTextLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.htm/",
                None,
                ptr.HtmlTableTextLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.asp",
                None,
                ptr.HtmlTableTextLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.aspx/",
                None,
                ptr.HtmlTableTextLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.json",
                None,
                ptr.JsonTableTextLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.jsonl",
                None,
                ptr.JsonLinesTableTextLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.ldjson",
                None,
                ptr.JsonLinesTableTextLoader,
            ],
            ["https://github.com/validext.ltsv", None, ptr.LtsvTableTextLoader],
            ["https://github.com/validext.md", None, ptr.MarkdownTableTextLoader],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.ndjson",
                None,
                ptr.JsonLinesTableTextLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.sqlite",
                None,
                ptr.SqliteFileLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.sqlite3",
                None,
                ptr.SqliteFileLoader,
            ],
            [
                "https://raw.githubusercontent.com/valid/test/data/validext.tsv",
                None,
                ptr.TsvTableTextLoader,
            ],
            ["https://github.com/validext.txt", "csv", ptr.CsvTableTextLoader],
            ["https://github.com/validext.txt", "html", ptr.HtmlTableTextLoader],
            ["https://github.com/validext.txt", "json", ptr.JsonTableTextLoader],
            ["https://github.com/validext.txt", "jsonl", ptr.JsonLinesTableTextLoader],
            ["https://github.com/validext.txt", "json_lines", ptr.JsonLinesTableTextLoader],
            ["https://github.com/validext.txt", "ldjson", ptr.JsonLinesTableTextLoader],
            ["https://github.com/invalidext.txt", "markdown", ptr.MarkdownTableTextLoader],
            ["https://github.com/invalidext.txt", "mediawiki", ptr.MediaWikiTableTextLoader],
            ["https://github.com/validext.txt", "ndjson", ptr.JsonLinesTableTextLoader],
            ["https://github.com/validext.txt", "tsv", ptr.TsvTableTextLoader],
        ],
    )
    def test_normal(self, value, format_name, expected):
        responses.add(
            responses.GET,
            value,
            body="""{}""",
            content_type="text/plain; charset=utf-8",
            status=200,
        )

        loader = ptr.TableUrlLoader(value, format_name)
        expected_loader = expected("")

        assert loader.source_type == expected_loader.source_type
        assert loader.format_name == expected_loader.format_name

    @responses.activate
    @pytest.mark.parametrize(
        ["value", "format_name", "expected"],
        [
            [None, None, ValueError],
            ["", None, ptr.UrlError],
            ["https://github.com/", None, ptr.UrlError],
            ["/tmp/test.txt", None, ptr.UrlError],
            ["c:\\tmp\test.txt", None, ptr.UrlError],
            [
                "https://raw.githubusercontent.com/invalid/test/data/invalidext.txt",
                None,
                ptr.LoaderNotFoundError,
            ],
            [
                "https://raw.githubusercontent.com/invalid/test/data/notexist.json",
                None,
                ptr.HTTPError,
            ],
            [
                "https://raw.githubusercontent.com/invalid/test/data/invalidext.txt",
                "invalidformat",
                ptr.LoaderNotFoundError,
            ],
        ],
    )
    def test_exception(self, value, format_name, expected):
        responses.add(responses.GET, value, body="""404: Not Found""", status=404)

        with pytest.raises(expected):
            ptr.TableUrlLoader(value, format_name)


class Test_TableUrlLoader_load:
    def setup_method(self, method):
        AbstractTableReader.clear_table_count()

    @responses.activate
    @pytest.mark.parametrize(
        ["url", "format_name"],
        [
            ["https://raw.githubusercontent.com/valid/test/data/validdata.csv", None],
            ["https://raw.githubusercontent.com/valid/test/data/validdata.txt", "csv"],
        ],
    )
    def test_normal_csv(self, url, format_name):
        responses.add(
            responses.GET,
            url,
            body=dedent(
                """\
                "attr_a","attr_b","attr_c"
                1,4,"a"
                2,2.1,"bb"
                3,120.9,"ccc"
                """
            ),
            content_type="text/plain; charset=utf-8",
            status=200,
        )
        expected_list = [
            TableData(
                "csv1",
                ["attr_a", "attr_b", "attr_c"],
                [[1, 4, "a"], [2, "2.1", "bb"], [3, "120.9", "ccc"]],
            )
        ]
        loader = ptr.TableUrlLoader(url, format_name)

        assert loader.format_name == "csv"

        for table_data in loader.load():
            assert table_data.in_tabledata_list(expected_list)

    @responses.activate
    @pytest.mark.parametrize(
        ["url", "format_name"],
        [
            ["https://raw.githubusercontent.com/valid/test/data/validdata.json", None],
            ["https://raw.githubusercontent.com/valid/test/data/validdata.txt", "json"],
        ],
    )
    def test_normal_json(self, url, format_name):
        responses.add(
            responses.GET,
            url,
            body=dedent(
                """\
                [
                    {"attr_a": 1},
                    {"attr_b": 2.1, "attr_c": "bb"}
                ]"""
            ),
            content_type="text/plain; charset=utf-8",
            status=200,
        )
        expected_list = [
            TableData(
                "url_loader",
                ["attr_a", "attr_b", "attr_c"],
                [{"attr_a": 1}, {"attr_b": 2.1, "attr_c": "bb"}],
            )
        ]

        loader = ptr.TableUrlLoader(url, format_name)
        assert loader.format_name == "json"

        loader.table_name = "url_loader"

        for table_data in loader.load():
            print(f"{table_data} {dumps_tabledata(table_data)}")
            print(table_data.rows)
            print("[expected]")
            for expected in expected_list:
                print(dumps_tabledata(expected))

            assert table_data.in_tabledata_list(expected_list)

    @pytest.mark.xfail(run=False)
    @responses.activate
    def test_normal_excel(self):
        url = "https://github.com/thombashi/valid/test/data/validdata.xlsx"
        data_path = os.path.join(dirname(dirname(__file__)), "data/validdata.xlsx")

        with open(data_path, "rb") as f:
            responses.add(
                responses.GET,
                url,
                body=f.read(),
                content_type="application/octet-stream",
                status=200,
            )

        expected_list = [
            TableData(
                "testsheet1",
                ["a1", "b1", "c1"],
                [["aa1", "ab1", "ac1"], [1.0, 1.1, "a"], [2.0, 2.2, "bb"], [3.0, 3.3, "cc"]],
            ),
            TableData(
                "testsheet3",
                ["a3", "b3", "c3"],
                [["aa3", "ab3", "ac3"], [4.0, 1.1, "a"], [5.0, "", "bb"], [6.0, 3.3, ""]],
            ),
        ]
        loader = ptr.TableUrlLoader(url)

        assert loader.format_name == "excel"

        for table_data in loader.load():
            assert table_data.in_tabledata_list(expected_list)

    @pytest.mark.xfail(run=False)
    @responses.activate
    def test_normal_sqlite(self):
        url = "https://github.com/thombashi/valid/test/data/valid.sqlite3"
        data_path = os.path.join(dirname(dirname(__file__)), "data/valid.sqlite3")

        with open(data_path, "rb") as f:
            responses.add(
                responses.GET,
                url,
                body=f.read(),
                content_type="application/octet-stream",
                status=200,
            )

        loader = ptr.TableUrlLoader(url)

        assert loader.format_name == "sqlite"

        for table_data in loader.load():
            assert table_data == TableData(
                "tblfaker",
                ["file_extension", "random_number"],
                [["webm", 679215], ["jpg", 5088743], ["avi", 8268]],
            )
