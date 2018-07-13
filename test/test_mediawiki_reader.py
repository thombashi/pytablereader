# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import collections
from textwrap import dedent

import pytablereader as ptr
import pytest
from path import Path
from pytablereader.interface import TableLoader
from pytablereader.mediawiki.formatter import MediaWikiTableFormatter
from tabledata import TableData


Data = collections.namedtuple("Data", "value expected")

test_data_empty = Data("""[]""", [TableData("tmp", [], [])])
test_data_01 = Data(
    dedent(
        """\
        hogehoge
        {| class="wikitable"
        ! a
        ! b
        ! c
        |-
        | style="text-align:right"| 1
        | style="text-align:right"| 123.1
        | a
        |-
        | style="text-align:right"| 2
        | style="text-align:right"| 2.2
        | bb
        |-
        | style="text-align:right"| 3
        | style="text-align:right"| 3.3
        | ccc
        |}
        """
    ),
    [
        TableData(
            table_name="mediawiki1",
            header_list=["a", "b", "c"],
            row_list=[["1", "123.1", "a"], ["2", "2.2", "bb"], ["3", "3.3", "ccc"]],
        )
    ],
)
test_data_02 = Data(
    dedent(
        """\
        {| class="wikitable"
        |+tablename
        ! a
        ! b
        ! c
        |-
        | style="text-align:right"| 1
        | style="text-align:right"| 123.1
        | a
        |-
        | style="text-align:right"| 2
        | style="text-align:right"| 2.2
        | bb
        |-
        | style="text-align:right"| 3
        | style="text-align:right"| 3.3
        | ccc
        |}
        """
    ),
    [
        TableData(
            table_name="tablename",
            header_list=["a", "b", "c"],
            row_list=[["1", "123.1", "a"], ["2", "2.2", "bb"], ["3", "3.3", "ccc"]],
        )
    ],
)
test_data_04 = Data(
    dedent(
        """\
        foobar
        {| class="wikitable"
        |+tablename
        ! a
        ! b
        ! c
        |-
        | style="text-align:right"| 1
        | style="text-align:right"| 123.1
        | a
        |-
        | style="text-align:right"| 2
        | style="text-align:right"| 2.2
        | bb
        |-
        | style="text-align:right"| 3
        | style="text-align:right"| 3.3
        | ccc
        |}
        {| class="wikitable"
        ! a
        ! b
        |-
        | style="text-align:right"| 1
        | style="text-align:right"| 123.1
        |-
        | style="text-align:right"| 2
        | style="text-align:right"| 2.2
        |-
        | style="text-align:right"| 3
        | style="text-align:right"| 3.3
        |}
        hogehoge
        """
    ),
    [
        TableData(
            table_name="tmp_tablename",
            header_list=["a", "b", "c"],
            row_list=[["1", "123.1", "a"], ["2", "2.2", "bb"], ["3", "3.3", "ccc"]],
        ),
        TableData(
            table_name="tmp_mediawiki2",
            header_list=["a", "b"],
            row_list=[["1", "123.1"], ["2", "2.2"], ["3", "3.3"]],
        ),
    ],
)
test_empty_data_00 = "= empty table ="
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


@pytest.mark.xfail(run=False)
class MediaWikiTableFormatter_constructor(object):
    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [["tablename", None, ptr.DataError], ["tablename", "", ptr.DataError]],
    )
    def test_exception(self, monkeypatch, value, source, expected):
        with pytest.raises(expected):
            MediaWikiTableFormatter(source)


@pytest.mark.xfail(run=False)
class Test_MediaWikiTableFormatter_make_table_name(object):
    def setup_method(self, method):
        TableLoader.clear_table_count()

    @property
    def valid_tag_property(self):
        return "mediawikitable"

    @property
    def null_tag_property(self):
        return None

    FILE_LOADER_TEST_DATA = [
        ["%(filename)s", "/path/to/data.mediawiki", "data"],
        ["prefix_%(filename)s", "/path/to/data.mediawiki", "prefix_data"],
        ["%(filename)s_suffix", "/path/to/data.mediawiki", "data_suffix"],
        ["prefix_%(filename)s_suffix", "/path/to/data.mediawiki", "prefix_data_suffix"],
        ["%(filename)s%(filename)s", "/path/to/data.mediawiki", "datadata"],
        ["%(format_name)s%(format_id)s_%(filename)s", "/path/to/data.mediawiki", "mediawiki0_data"],
    ]

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [["%(default)s", "/path/to/data.mediawiki", "data_mediawikitable"]] + FILE_LOADER_TEST_DATA,
    )
    def test_normal_MediaWikiTableFileLoader_valid_tag(self, monkeypatch, value, source, expected):
        monkeypatch.setattr(MediaWikiTableFormatter, "table_id", self.valid_tag_property)

        loader = ptr.MediaWikiTableFileLoader(source)
        loader.table_name = value
        formatter = MediaWikiTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(default)s", "/path/to/data.mediawiki", "data_mediawiki0"],
            ["%(%(filename)s)", "/path/to/data.mediawiki", "%(data)"],
        ]
        + FILE_LOADER_TEST_DATA,
    )
    def test_normal_MediaWikiTableFileLoader_null_tag(self, monkeypatch, value, source, expected):
        monkeypatch.setattr(MediaWikiTableFormatter, "table_id", self.null_tag_property)

        loader = ptr.MediaWikiTableFileLoader(source)
        loader.table_name = value
        formatter = MediaWikiTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            [None, "/path/to/data.mediawiki", ValueError],
            ["", "/path/to/data.mediawiki", ValueError],
        ],
    )
    def test_MediaWikiTableFileLoader_exception(self, monkeypatch, value, source, expected):
        monkeypatch.setattr(MediaWikiTableFormatter, "table_id", self.null_tag_property)

        loader = ptr.MediaWikiTableFileLoader(source)
        loader.table_name = value
        formatter = MediaWikiTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            formatter._make_table_name()

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["%(default)s", "mediawikitable"],
            ["%(key)s", "mediawikitable"],
            ["%(format_name)s%(format_id)s", "mediawiki0"],
            ["%(filename)s%(format_name)s%(format_id)s", "mediawiki0"],
            ["tablename", "tablename"],
        ],
    )
    def test_normal_MediaWikiTableTextLoader_valid_tag(self, monkeypatch, value, expected):
        monkeypatch.setattr(MediaWikiTableFormatter, "table_id", self.valid_tag_property)

        source = "<table></table>"
        loader = ptr.MediaWikiTableTextLoader(source)
        loader.table_name = value
        formatter = MediaWikiTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["%(default)s", "mediawiki0"],
            ["%(key)s", "mediawiki0"],
            ["%(format_name)s%(format_id)s", "mediawiki0"],
            ["%(filename)s%(format_name)s%(format_id)s", "mediawiki0"],
            ["tablename", "tablename"],
        ],
    )
    def test_normal_MediaWikiTableTextLoader_null_tag(self, monkeypatch, value, expected):
        monkeypatch.setattr(MediaWikiTableFormatter, "table_id", self.null_tag_property)

        source = "<table></table>"
        loader = ptr.MediaWikiTableTextLoader(source)
        loader.table_name = value
        formatter = MediaWikiTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            [None, "<table></table>", ValueError],
            ["%(filename)s", "<table></table>", ptr.InvalidTableNameError],
        ],
    )
    def test_exception_MediaWikiTableTextLoader(self, monkeypatch, value, source, expected):
        monkeypatch.setattr(MediaWikiTableFormatter, "table_id", self.valid_tag_property)

        loader = ptr.MediaWikiTableTextLoader(source)
        loader.table_name = value
        formatter = MediaWikiTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            print(formatter._make_table_name())


@pytest.mark.xfail(run=False)
class Test_MediaWikiTableFileLoader_load(object):
    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        ["test_id", "table_text", "filename", "table_name", "expected_tabledata_list"],
        [
            [1, test_data_01.value, "tmp.mediawiki", "%(key)s", test_data_01.expected],
            [2, test_data_02.value, "tmp.mediawiki", "%(key)s", test_data_02.expected],
            [4, test_data_04.value, "tmp.mediawiki", "%(default)s", test_data_04.expected],
        ],
    )
    def test_normal(
        self, tmpdir, test_id, table_text, filename, table_name, expected_tabledata_list
    ):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        with open(file_path, "w") as f:
            f.write(table_text)

        loader = ptr.MediaWikiTableFileLoader(file_path)
        loader.table_name = table_name

        load = False
        for tabledata, expected in zip(loader.load(), expected_tabledata_list):
            print("--- test {} ---".format(test_id))
            print("[tabledata]\n{}".format(tabledata))
            print("[expected]\n{}".format(expected))
            print("")
            assert tabledata == expected

            load = True

        assert load

    @pytest.mark.parametrize(
        ["table_text", "filename", "expected"],
        [
            [test_empty_data_00, "tmp.mediawiki", ptr.DataError],
            [test_empty_data_01, "tmp.mediawiki", ptr.DataError],
        ],
    )
    def test_normal_empty_data(self, tmpdir, table_text, filename, expected):
        p_file_path = tmpdir.join(filename)

        with open(str(p_file_path), "w") as f:
            f.write(table_text)

        loader = ptr.MediaWikiTableFileLoader(str(p_file_path))

        for _tabletuple in loader.load():
            raise ValueError("should not reach this line")

    @pytest.mark.parametrize(
        ["filename", "expected"], [["", ptr.InvalidFilePathError], [None, ptr.InvalidFilePathError]]
    )
    def test_exception_null(self, tmpdir, filename, expected):
        loader = ptr.MediaWikiTableFileLoader(filename)

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


@pytest.mark.xfail(run=False)
class Test_MediaWikiTableTextLoader_load(object):
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
        loader = ptr.MediaWikiTableTextLoader(table_text)
        loader.table_name = table_name

        load = False
        for tabledata in loader.load():
            print("--- id {} ---".format(test_id))
            print("[tabledata]\n{}".format(tabledata))
            print("[expected]")
            for expected in expected_tabletuple_list:
                print("    {}".format(expected))
            print("")

            assert tabledata in expected_tabletuple_list

            load = True

        assert load

    @pytest.mark.parametrize(["table_text"], [[test_empty_data_00], [test_empty_data_01]])
    def test_normal_empty_data(self, table_text):
        loader = ptr.MediaWikiTableTextLoader(table_text)
        loader.table_name = "dummy"

        for _tabletuple in loader.load():
            raise ValueError("should not reach this line")

    @pytest.mark.parametrize(
        ["table_text", "expected"], [["", ptr.DataError], [None, ptr.DataError]]
    )
    def test_null(self, table_text, expected):
        loader = ptr.MediaWikiTableTextLoader(table_text)
        loader.table_name = "dummy"

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
