# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals
import io
import collections

from path import Path
import pytablewriter as ptw
import pytest

import pytablereader as ptr
from pytablereader.interface import TableLoader
from pytablereader import TableData
from pytablereader.html.formatter import HtmlTableFormatter


Data = collections.namedtuple("Data", "value table_name expected")

test_data_empty = Data(
    """[]""",
    "",
    [
        TableData("tmp", [], []),
    ])

test_data_01 = Data(
    value="""<title>title</title>
<table>
  <thead>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
    </tr>
  </tbody>
</table>
""",
    table_name="%(default)s",
    expected=[
        TableData(
            table_name="title_html1",
            header_list=['a', 'b', 'c'],
            record_list=[
                [1, '123.1', 'a'],
                [2, '2.2', 'bb'],
                [3, '3.3', 'ccc'],
            ]
        ),
    ])

test_data_02 = Data(
    value="""<title>hoge</title>
<table id="tablename">
    <caption>caption</caption>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
    </tr>
</table>
""",
    table_name="%(key)s",
    expected=[
        TableData(
            table_name="tablename",
            header_list=['a', 'b', 'c'],
            record_list=[
                [1, '123.1', 'a'],
                [2, '2.2', 'bb'],
                [3, '3.3', 'ccc'],
            ]
        ),
    ])

test_data_03 = Data(
    value="""
<html>
  <head>
    header
  </head>
  <body>
    hogehoge
  </body>
</html>
""",
    table_name="%(default)s",
    expected=[])

test_data_04 = Data(
    value="""<title>test_data_04</title>
<table id="tablename">
    <caption>caption</caption>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
    </tr>
</table>

<table>
</table>

<table>
    <tr></tr>
    <tr></tr>
</table>

<table class="img_right_top"  width="258" >
 <tr class="odd">
  <td style="width:258px;">
    <a href="./screenshot.html?num=001" target="_blank" style="text-decoration: none;">
    link text
    </a>
  </td>
 </tr>
</table>

<table>
    <tr>
      <th>a</th>
      <th>b</th>
    </tr>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
    </tr>
</table>
""",
    table_name="%(default)s",
    expected=[
        TableData(
            table_name="test_data_04_tablename",
            header_list=['a', 'b', 'c'],
            record_list=[
                [1, '123.1', 'a'],
                [2, '2.2', 'bb'],
                [3, '3.3', 'ccc'],
            ]
        ),
        TableData(
            table_name="test_data_04_html2",
            header_list=[],
            record_list=[
                ['link text'],
            ]
        ),
        TableData(
            table_name="test_data_04_html3",
            header_list=['a', 'b'],
            record_list=[
                [1, '123.1'],
                [2, '2.2'],
                [3, '3.3'],
            ]
        ),
    ])

test_data_05 = Data(
    value="""<table>
  <caption>captiontest</caption>
  <thead>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
    </tr>
  </tbody>
</table>
""",
    table_name="%(default)s",
    expected=[
        TableData(
            table_name="captiontest",
            header_list=['a', 'b', 'c'],
            record_list=[
                [1, '123.1', 'a'],
                [2, '2.2', 'bb'],
                [3, '3.3', 'ccc'],
            ]
        ),
    ])

test_data_06 = Data(
    value="""<title>test_data_06</title>
<table class="prettytable inflection-table">
<tr>
<th style="background:#549EA0; font-style:italic;">Case</th>
<th style="background:#549EA0; font-style:italic;">Singular</th>
<th style="background:#549EA0; font-style:italic;">Plural</th>
</tr>
<tr>
<th style="background:#40E0D0; font-style:italic;"><a href="/wiki/nominative_case" title="nominative case">nominative</a></th>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><strong class="selflink">val01</strong></span></td>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythones#Latin" title="pythones">val02</a></span></td>
</tr>
<tr>
<th style="background:#40E0D0; font-style:italic;"><a href="/wiki/genitive_case" title="genitive case">genitive</a></th>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythonis#Latin" title="pythonis">val11</a></span></td>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythonum#Latin" title="pythonum">val12</a></span></td>
</tr>
<tr>
<th style="background:#40E0D0; font-style:italic;"><a href="/wiki/dative_case" title="dative case">dative</a></th>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythoni#Latin" title="pythoni">val21</a></span></td>
<td style="background:#F8F8FF;"><span class="Latn" lang="la" xml:lang="la"><a href="/wiki/pythonibus#Latin" title="pythonibus">val22</a></span></td>
</tr>
</table>
""",
    table_name="%(default)s",
    expected=[
        TableData(
            table_name="test_data_06_html1",
            header_list=["Case", "Singular", "Plural"],
            record_list=[
                ["nominative", "val01", "val02"],
                ["genitive", "val11", "val12"],
                ["dative", "val21", "val22"],
            ]
        ),
    ])

test_data_07 = Data(
    value="""
            <div class="locale-selection-panel site-flag site-flag-lang" style="top: -245px; display: none;">
                <div class="content" role="menu">
                    <table class="all-locales" cellspacing="0" autogeneratecolumns="false" allowpaging="false" allowsorting="false" style="border-collapse: collapse;">
                        <tbody>
                            <tr>
                                    <td><a title="Deutsch" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=de-de&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">Deutsch</a></td>
                                    <td><a title="English" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=en-us&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">English</a></td>
                                    <td><a title="Español" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=es-es&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">Español</a></td>
                                    <td><a title="Français" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=fr-fr&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">Français</a></td>
                            </tr><tr>
                                    <td><a title="Italiano" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=it-it&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">Italiano</a></td>
                                    <td><a title="日本語" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=ja-jp&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link selected" role="menuitem">日本語</a></td>
                                    <td><a title="한국어" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=ko-kr&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">한국어</a></td>
                                    <td><a title="Português" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=pt-br&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">Português</a></td>
                            </tr><tr>
                                    <td><a title="" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=ru-ru&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">Pусский</a></td>
                                    <td><a title="简体中文" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=zh-cn&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">简体中文</a></td>
                                    <td><a title="繁體中文" href="https://msdn.microsoft.com/ja-jp/?action=selectlocale&amp;currentlocale=ja-jp&amp;newlocale=zh-tw&amp;frompage=/ja-jp/library/windows/desktop/hh802691" class="locale-link" role="menuitem">繁體中文</a></td>
                                    <td></td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="arrow">
                         </div>
                </div>
            </div>
""",
    table_name="%(default)s",
    expected=[
        TableData(
            table_name="html1",
            header_list=[],
            record_list=[
                ["Deutsch", "English", "Español", "Français"],
                ["Italiano", "日本語", "한국어", "Português"],
                ["Pусский", "简体中文", "繁體中文", ""],
            ]
        ),
    ])


class HtmlTableFormatter_constructor(object):

    @pytest.mark.parametrize(["value", "source", "expected"], [
        ["tablename", None, ptr.InvalidDataError],
        ["tablename", "", ptr.InvalidDataError],
    ])
    def test_exception(
            self, monkeypatch, value, source, expected):
        with pytest.raises(expected):
            HtmlTableFormatter(source)


class Test_HtmlTableFormatter_make_table_name:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @property
    def valid_tag_property(self):
        return "htmltable"

    @property
    def null_tag_property(self):
        return None

    FILE_LOADER_TEST_DATA = [
        ["%(filename)s", "/path/to/data.html", "data"],
        ["prefix_%(filename)s",  "/path/to/data.html", "prefix_data"],
        ["%(filename)s_suffix", "/path/to/data.html", "data_suffix"],
        [
            "prefix_%(filename)s_suffix",
            "/path/to/data.html",
            "prefix_data_suffix"
        ],
        [
            "%(filename)s%(filename)s",
            "/path/to/data.html",
            "datadata"
        ],
        [
            "%(format_name)s%(format_id)s_%(filename)s",
            "/path/to/data.html",
            "html0_data"
        ],
    ]

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            ["%(default)s",  "/path/to/data.html", "htmltable"],
        ] + FILE_LOADER_TEST_DATA)
    def test_normal_HtmlTableFileLoader_valid_tag(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.valid_tag_property)

        loader = ptr.HtmlTableFileLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(
        ["value", "source", "expected"],
        [
            [
                "%(%(filename)s)",
                "/path/to/data.html",
                "%(data)"
            ],
            ["%(default)s",  "/path/to/data.html", "html0"],
        ] + FILE_LOADER_TEST_DATA)
    def test_normal_HtmlTableFileLoader_null_tag(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.null_tag_property)

        loader = ptr.HtmlTableFileLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(value)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "/path/to/data.html", ValueError],
        ["", "/path/to/data.html", ValueError],
    ])
    def test_HtmlTableFileLoader_exception(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.null_tag_property)

        loader = ptr.HtmlTableFileLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            formatter._make_table_name()

    @pytest.mark.parametrize(["value", "expected"], [
        ["%(default)s", "validtag_htmltable"],
        ["%(key)s", "htmltable"],
        ["%(format_name)s%(format_id)s", "html0"],
        ["%(filename)s%(format_name)s%(format_id)s", "html0"],
        ["tablename", "tablename"],
    ])
    def test_normal_HtmlTableTextLoader_valid_tag(
            self, monkeypatch, value, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.valid_tag_property)

        source = """
        <title>validtag</title>
        <table></table>
        """
        loader = ptr.HtmlTableTextLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["%(default)s", "nulltag_html0"],
        ["%(key)s", "html0"],
        ["%(format_name)s%(format_id)s", "html0"],
        ["%(filename)s%(format_name)s%(format_id)s", "html0"],
        ["tablename", "tablename"],
    ])
    def test_normal_HtmlTableTextLoader_null_tag(
            self, monkeypatch, value, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.null_tag_property)

        source = """
        <title>nulltag</title>
        <table></table>
        """
        loader = ptr.HtmlTableTextLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(source)
        formatter.accept(loader)

        assert formatter._make_table_name() == expected

    @pytest.mark.parametrize(["value", "source", "expected"], [
        [None, "<table></table>", ValueError],
        [
            "%(filename)s",
            "<table></table>",
            ptr.InvalidTableNameError
        ],
    ])
    def test_exception_HtmlTableTextLoader(
            self, monkeypatch, value, source, expected):
        monkeypatch.setattr(
            HtmlTableFormatter, "table_id", self.valid_tag_property)

        loader = ptr.HtmlTableTextLoader(source)
        loader.table_name = value
        formatter = HtmlTableFormatter(source)
        formatter.accept(loader)

        with pytest.raises(expected):
            print(formatter._make_table_name())


class Test_HtmlTableFileLoader_load:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        [
            "test_id",
            "table_text",
            "filename",
            "table_name",
            "expected_tabledata_list",
        ],
        [
            [
                1, test_data_01.value, "tmp1.html",
                test_data_01.table_name,
                test_data_01.expected
            ],
            [
                2, test_data_02.value, "tmp2.html",
                test_data_02.table_name,
                test_data_02.expected,
            ],
            [
                3, test_data_03.value, "tmp3.html",
                test_data_03.table_name,
                test_data_03.expected,
            ],
            [
                4, test_data_04.value, "tmp4.html",
                test_data_04.table_name,
                test_data_04.expected,
            ],
            [
                5, test_data_05.value, "tmp5.html",
                test_data_05.table_name,
                test_data_05.expected,
            ],
            [
                6, test_data_06.value, "tmp6.html",
                test_data_06.table_name,
                test_data_06.expected,
            ],
            [
                7, test_data_07.value, "tmp7.html",
                test_data_07.table_name,
                test_data_07.expected,
            ],
        ])
    def test_normal(
            self, tmpdir, test_id, table_text, filename,
            table_name, expected_tabledata_list):
        file_path = Path(str(tmpdir.join(filename)))
        file_path.parent.makedirs_p()

        with io.open(file_path, "w", encoding="utf-8") as f:
            f.write(table_text)

        loader = ptr.HtmlTableFileLoader(file_path)
        loader.table_name = table_name

        for tabledata, expected in zip(loader.load(), expected_tabledata_list):
            print("[test {}]".format(test_id))
            print("expected: {}".format(ptw.dump_tabledata(expected)))
            print("actusl: {}".format(ptw.dump_tabledata(tabledata)))
            print("")

            assert tabledata == expected

    @pytest.mark.parametrize(
        [
            "table_text",
            "filename",
            "expected",
        ],
        [
            [
                "",
                "tmp.html",
                ptr.InvalidDataError,
            ],
        ])
    def test_exception_invalid_data(
            self, tmpdir, table_text, filename, expected):
        p_file_path = tmpdir.join(filename)

        with open(str(p_file_path), "w") as f:
            f.write(table_text)

        loader = ptr.HtmlTableFileLoader(str(p_file_path))

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass

    @pytest.mark.parametrize(["filename", "expected"], [
        ["", IOError],
        [None, IOError],
    ])
    def test_exception_null_filename(
            self, tmpdir, filename, expected):
        loader = ptr.HtmlTableFileLoader(filename)

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass


class Test_HtmlTableTextLoader_load:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(
        [
            "table_text",
            "table_name",
            "expected_tabletuple_list",
        ],
        [
            [
                test_data_01.value,
                test_data_01.table_name,
                test_data_01.expected,
            ],
            [
                test_data_02.value,
                test_data_02.table_name,
                test_data_02.expected,
            ],
            [
                test_data_03.value,
                test_data_03.table_name,
                test_data_03.expected,
            ],
        ])
    def test_normal(self, table_text, table_name, expected_tabletuple_list):
        loader = ptr.HtmlTableTextLoader(table_text)
        loader.table_name = table_name

        for tabledata in loader.load():
            print("actusl: {}".format(ptw.dump_tabledata(tabledata)))

            assert tabledata in expected_tabletuple_list

    @pytest.mark.parametrize(["table_text", "expected"], [
        ["", ptr.InvalidDataError],
        [None, ptr.InvalidDataError],
    ])
    def test_exception_null(self, table_text, expected):
        loader = ptr.HtmlTableTextLoader(table_text)
        loader.table_name = "dummy"

        with pytest.raises(expected):
            for _tabletuple in loader.load():
                pass
