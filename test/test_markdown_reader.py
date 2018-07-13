# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import collections
from textwrap import dedent

import pytablereader as ptr
import pytablewriter as ptw
import pytest
from path import Path
from pytablereader.interface import TableLoader
from pytablereader.markdown.formatter import MarkdownTableFormatter
from tabledata import TableData


Data = collections.namedtuple("Data", "value expected")

test_data_empty = Data("""[]""", [TableData("tmp", [], [])])

test_data_01 = Data(
    dedent(
        """\
        | a |  b  | c |
        |--:|----:|---|
        |  1|123.1|a  |
        |  2|  2.2|bb |
        |  3|  3.3|ccc|
        """
    ),
    [
        TableData(
            table_name="markdown1",
            header_list=["a", "b", "c"],
            row_list=[[1, "123.1", "a"], [2, "2.2", "bb"], [3, "3.3", "ccc"]],
        )
    ],
)
test_data_02 = Data(
    dedent(
        """\
        # tablename
        | a |  b  | c |
        |--:|----:|---|
        |  1|123.1|a  |
        |  2|  2.2|bb |
        |  3|  3.3|ccc|
        """
    ),
    [
        TableData(
            table_name="markdown1",
            header_list=["a", "b", "c"],
            row_list=[[1, "123.1", "a"], [2, "2.2", "bb"], [3, "3.3", "ccc"]],
        )
    ],
)
test_data_04 = Data(
    dedent(
        """\
        # tablename
        | a |  b  | c |
        |--:|----:|---|
        |  1|123.1|a  |
        |  2|  2.2|bb |
        |  3|  3.3|ccc|

        # tmp_markdown2|
        | a |  b  |
        |--:|----:|
        |  1|123.1|
        |  2|  2.2|
        |  3|  3.3|
        """
    ),
    [
        TableData(
            table_name="tmp_markdown1",
            header_list=["a", "b", "c"],
            row_list=[[1, "123.1", "a"], [2, "2.2", "bb"], ["3", "3.3", "ccc"]],
        ),
        TableData(
            table_name="tmp_markdown2",
            header_list=["a", "b"],
            row_list=[[1, "123.1"], [2, "2.2"], ["3", "3.3"]],
        ),
    ],
)

test_empty_data_00 = "# empty table"
test_empty_data_01 = dedent(
    """\
    <html>
    <head>
        header
    </head>
    <body>
        hogehoge
    </body>
    </html>
    """
)


class MarkdownTableFormatter_constructor(object):
    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [["tablename", None, ptr.DataError], ["tablename", "", ptr.DataError]],
    )
    def test_exception(self, monkeypatch, value, source, expected):
        with pytest.raises(expected):
            MarkdownTableFormatter(source)


class Test_MarkdownTableFormatter_make_table_name(object):
    def setup_method(self, method):
        TableLoader.clear_table_count()

    @property
    def valid_tag_property(self):
        return "markdowntable"

    @property
    def null_tag_property(self):
        return None

    FILE_LOADER_TEST_DATA = [
        ["%(filename)s", "/path/to/data.markdown", "data"],
        ["prefix_%(filename)s", "/path/to/data.md", "prefix_data"],
        ["%(filename)s_suffix", "/path/to/data.md", "data_suffix"],
        ["prefix_%(filename)s_suffix", "/path/to/data.md", "prefix_data_suffix"],
        ["%(filename)s%(filename)s", "/path/to/data.md", "datadata"],
        ["%(format_name)s%(format_id)s_%(filename)s", "/path/to/data.md", "markdown0_data"],
    ]

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [["%(default)s", "/path/to/data.md", "data_markdowntable"]] + FILE_LOADER_TEST_DATA,
    )
    def test_normal_MarkdownTableFileLoader_valid_tag(self, monkeypatch, value, source, expected):
        monkeypatch.setattr(MarkdownTableFormatter, "table_id", self.valid_tag_property)

        loader = ptr.MarkdownTableFileLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(default)s", "/path/to/data.md", "data_markdown0"],
            ["%(%(filename)s)", "/path/to/data.md", "%(data)"],
        ]
        + FILE_LOADER_TEST_DATA,
    )
    def test_normal_MarkdownTableFileLoader_null_tag(self, monkeypatch, value, source, expected):
        monkeypatch.setattr(MarkdownTableFormatter, "table_id", self.null_tag_property)

        loader = ptr.MarkdownTableFileLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [[None, "/path/to/data.md", ValueError], ["", "/path/to/data.md", ValueError]],
    )
    def test_MarkdownTableFileLoader_exception(self, monkeypatch, value, source, expected):
        monkeypatch.setattr(MarkdownTableFormatter, "table_id", self.null_tag_property)

        loader = ptr.MarkdownTableFileLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            formatter._make_table_name()

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["%(default)s", "markdowntable"],
            ["%(key)s", "markdowntable"],
            ["%(format_name)s%(format_id)s", "markdown0"],
            ["%(filename)s%(format_name)s%(format_id)s", "markdown0"],
            ["tablename", "tablename"],
        ],
    )
    def test_normal_MarkdownTableTextLoader_valid_tag(self, monkeypatch, value, expected):
        monkeypatch.setattr(MarkdownTableFormatter, "table_id", self.valid_tag_property)

        source = "<table></table>"
        loader = ptr.MarkdownTableTextLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["%(default)s", "markdown0"],
            ["%(key)s", "markdown0"],
            ["%(format_name)s%(format_id)s", "markdown0"],
            ["%(filename)s%(format_name)s%(format_id)s", "markdown0"],
            ["tablename", "tablename"],
        ],
    )
    def test_normal_MarkdownTableTextLoader_null_tag(self, monkeypatch, value, expected):
        monkeypatch.setattr(MarkdownTableFormatter, "table_id", self.null_tag_property)

        source = "<table></table>"
        loader = ptr.MarkdownTableTextLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            [None, "<table></table>", ValueError],
            ["%(filename)s", "<table></table>", ptr.InvalidTableNameError],
        ],
    )
    def test_exception_MarkdownTableTextLoader(self, monkeypatch, value, source, expected):
        monkeypatch.setattr(MarkdownTableFormatter, "table_id", self.valid_tag_property)

        loader = ptr.MarkdownTableTextLoader(source)
        loader.table_name = value
        formatter = MarkdownTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            print(formatter._make_table_name())


class Test_MarkdownTableFileLoader_load(object):
    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        ["test_id", "table_text", "filename", "table_name", "expected_tabledata_list"],
        [
            [1, test_data_01.value, "tmp.md", "%(key)s", test_data_01.expected],
            [2, test_data_02.value, "tmp.md", "%(key)s", test_data_02.expected],
            [4, test_data_04.value, "tmp.md", "%(default)s", test_data_04.expected],
        ],
    )
    def test_normal(
        self, tmpdir, test_id, table_text, filename, table_name, expected_tabledata_list
    ):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        with open(file_path, "w") as f:
            f.write(table_text)

        loader = ptr.MarkdownTableFileLoader(file_path)
        loader.table_name = table_name

        load = False
        for table_data in loader.load():
            print("--- test {} ---".format(test_id))
            print("\n[actual]\n{}".format(ptw.dump_tabledata(table_data)))
            assert table_data.in_tabledata_list(expected_tabledata_list)
            load = True

        assert load

    @pytest.mark.parametrize(
        ["table_text", "filename"], [[test_empty_data_00, "tmp.md"], [test_empty_data_01, "tmp.md"]]
    )
    def test_normal_empty_data(self, tmpdir, table_text, filename):
        p_file_path = tmpdir.join(filename)

        with open(str(p_file_path), "w") as f:
            f.write(table_text)

        loader = ptr.MarkdownTableFileLoader(str(p_file_path))

        for _tabletuple in loader.load():
            raise ValueError("should not reach this line")

    @pytest.mark.parametrize(
        ["filename", "expected"], [["", ptr.InvalidFilePathError], [None, ptr.InvalidFilePathError]]
    )
    def test_exception(self, tmpdir, filename, expected):
        loader = ptr.MarkdownTableFileLoader(filename)

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


class Test_MarkdownTableTextLoader_load(object):
    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        ["test_id", "table_text", "table_name", "expected_tabletuple_list"],
        [
            [1, test_data_01.value, "%(default)s", test_data_01.expected],
            [2, test_data_02.value, "%(default)s", test_data_02.expected],
        ],
    )
    def test_normal(self, test_id, table_text, table_name, expected_tabletuple_list):
        loader = ptr.MarkdownTableTextLoader(table_text)
        loader.table_name = table_name

        load = False
        for table_data in loader.load():
            print("--- id: {} ---".format(test_id))
            print("[actual]\n{}".format(table_data))
            print("[expected]")
            for expected in expected_tabletuple_list:
                print("    {}".format(expected))
            print("")
            assert table_data.in_tabledata_list(expected_tabletuple_list)

            load = True

        assert load

    @pytest.mark.parametrize(["table_text", "expected"], [["", ptr.DataError]])
    def test_exception_invalid_data(self, table_text, expected):
        loader = ptr.MarkdownTableTextLoader(table_text)
        loader.table_name = "dummy"

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(
        ["table_text", "expected"], [["", ptr.DataError], [None, ptr.DataError]]
    )
    def test_exception_null(self, table_text, expected):
        loader = ptr.MarkdownTableTextLoader(table_text)
        loader.table_name = "dummy"

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
