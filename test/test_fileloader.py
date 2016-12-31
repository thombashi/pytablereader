# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

from mbstrdecoder import MultiByteStrDecoder
from path import Path
import pytablewriter as ptw
import pytest
import six

import pathvalidate as pv
import pytablereader as ptr
from pytablereader.interface import TableLoader


class Test_TableFileLoader_constructor:

    @pytest.mark.parametrize(["file_path", "format_name", "expected"], [
        [
            "/tmp/valid/test/data/validext.csv",
            None, ptr.CsvTableFileLoader
        ],
        [
            "/tmp/valid/test/新しいフォルダー/新しいテキスト ドキュメント.csv".encode("utf_8"),
            None, ptr.CsvTableFileLoader
        ],
        [
            "/tmp/valid/test/data/validext.xlsx",
            None, ptr.ExcelTableFileLoader
        ],
        [
            "/tmp/valid/test/data/validext.html",
            None, ptr.HtmlTableFileLoader
        ],
        [
            "/tmp/valid/test/data/validext.json",
            None, ptr.JsonTableFileLoader
        ],
        ["/tmp/validext.txt", "csv", ptr.CsvTableFileLoader],
        ["/tmp/テスト.txt".encode("utf_8"), "csv", ptr.CsvTableFileLoader],
        ["/tmp/validext.txt", "html", ptr.HtmlTableFileLoader],
        ["/tmp/validext.txt", "json", ptr.JsonTableFileLoader],
        [
            "/tmp/invalidext.txt",
            "markdown", ptr.MarkdownTableFileLoader
        ],
        [
            "/tmp/invalidext.txt",
            "mediawiki", ptr.MediaWikiTableFileLoader
        ],
    ])
    def test_normal(self, tmpdir, file_path, format_name, expected):
        test_file_path = Path(six.text_type(tmpdir.join(
            Path(MultiByteStrDecoder(file_path).unicode_str))))
        test_file_path.parent.makedirs_p()

        with open(test_file_path, "w") as f:
            f.write('''{}''')

        loader = ptr.TableFileLoader(test_file_path, format_name)
        expected_loader = expected("")

        assert loader.source_type == expected_loader.source_type
        assert loader.format_name == expected_loader.format_name

    @pytest.mark.parametrize(["value", "format_name", "expected"], [
        [None, None, ptr.InvalidFilePathError],
        ["", None, ptr.InvalidFilePathError],
        ["https://github.com/", None, ptr.LoaderNotFoundError],
        ["/tmp/test.txt", None, ptr.LoaderNotFoundError],
        ["c:\\tmp\test.txt", None, ptr.LoaderNotFoundError],
        [
            "/tmp/valid/test/data/validext.csv/",
            None, ptr.LoaderNotFoundError
        ],
        [
            "/tmp/invalid/test/data/invalidext.txt",
            "invalidformat", ptr.LoaderNotFoundError
        ],
    ])
    def test_exception(self, value, format_name, expected):
        with pytest.raises(expected):
            ptr.TableFileLoader(value, format_name)


class Test_TableFileLoader_load:

    def setup_method(self, method):
        TableLoader.clear_table_count()

    @pytest.mark.parametrize(["file_path", "format_name"], [
        [
            '/tmp/valid/test/data/validdata.csv',
            None,
        ],
        [
            '/tmp/valid/test/data/validdata.txt',
            "csv",
        ],
    ])
    def test_normal_csv(self,  tmpdir, file_path, format_name):
        filename = pv.replace_symbol(file_path, "")
        p_file_path = Path(
            six.text_type(tmpdir.join(filename + Path(file_path).ext)))
        p_file_path.parent.makedirs_p()

        with open(p_file_path, "w") as f:
            f.write('''"attr_a","attr_b","attr_c"
    1,4,"a"
    2,2.1,"bb"
    3,120.9,"ccc"''')

        expeced_list = [
            ptr.TableData(
                filename,
                ["attr_a", "attr_b", "attr_c"],
                [
                    [1, 4,      "a"],
                    [2, "2.1",    "bb"],
                    [3, "120.9",  "ccc"],
                ])
        ]

        loader = ptr.TableFileLoader(p_file_path, format_name)

        assert loader.format_name == "csv"

        for tabledata, expected in zip(loader.load(), expeced_list):
            print(ptw.dump_tabledata(expected))
            print(ptw.dump_tabledata(tabledata))

            assert tabledata == expected

    @pytest.mark.parametrize(["file_path", "format_name"], [
        [
            '/tmp/valid/test/data/validdata.json',
            None,
        ],
        [
            '/tmp/valid/test/data/validdata.txt',
            "json",
        ],
    ])
    def test_normal_json(self, tmpdir, file_path, format_name):
        p_file_path = Path(str(tmpdir.join(file_path)))
        p_file_path.parent.makedirs_p()

        with open(p_file_path, "w") as f:
            f.write('''[
        {"attr_a": 1},
        {"attr_b": 2.1, "attr_c": "bb"}
    ]''')

        expeced_list = [
            ptr.TableData(
                "validdata_json1",
                ["attr_a", "attr_b", "attr_c"],
                [
                    {'attr_a': 1},
                    {'attr_b': 2.1, 'attr_c': 'bb'},
                ]
            )
        ]

        loader = ptr.TableFileLoader(p_file_path, format_name)

        assert loader.format_name == "json"

        for tabledata, expected in zip(loader.load(), expeced_list):
            assert tabledata == expected

    def test_normal_excel(self, tmpdir):
        file_path = '/tmp/valid/test/data/validdata.xlsx'
        p_file_path = Path(str(tmpdir.join(file_path)))
        p_file_path.parent.makedirs_p()

        tabledata_list = [
            ptr.TableData(
                table_name='testsheet1',
                header_list=['a1', 'b1', 'c1'],
                record_list=[
                    ['aa1', 'ab1', 'ac1'],
                    [1.0, 1.1, 'a'],
                    [2.0, 2.2, 'bb'],
                    [3.0, 3.3, 'cc'],
                ]),
            ptr.TableData(
                table_name='testsheet3',
                header_list=['a3', 'b3', 'c3'],
                record_list=[
                    ['aa3', 'ab3', 'ac3'],
                    [4.0, 1.1, 'a'],
                    [5.0, '', 'bb'],
                    [6.0, 3.3, ''],
                ]),
        ]

        writer = ptw.ExcelXlsxTableWriter()
        writer.open_workbook(p_file_path)
        for tabledata in tabledata_list:
            writer.from_tabledata(tabledata)
        writer.write_table()
        writer.close()

        loader = ptr.TableFileLoader(p_file_path)

        assert loader.format_name == "excel"

        for tabledata in loader.load():
            assert tabledata in tabledata_list
