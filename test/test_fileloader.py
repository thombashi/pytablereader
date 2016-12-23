# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function

from path import Path
import pytablewriter as ptw
import pytest

import pathvalidate as pv
import pytablereader as ptr
from pytablereader.interface import TableLoader
import pytablewriter as ptw


class Test_TableFileLoader_constructor:

    @pytest.mark.parametrize(["file_path", "format_name", "expected"], [
        [
            "/tmp/valid/test/data/validext.csv",
            None, ptr.CsvTableFileLoader
        ],
        [
            "c:\\tmp\valid\test\data\validext.csv",
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
        [
            "https://github.com/validext.md",
            None, ptr.MarkdownTableFileLoader
        ],
        ["/tmp/validext.txt", "csv", ptr.CsvTableFileLoader],
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
        test_file_path = Path(str(tmpdir.join(
            pv.replace_symbol(file_path, "") + Path(file_path).ext)))
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
        p_file_path = Path(str(tmpdir.join(filename + Path(file_path).ext)))
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
                    {u'attr_a': 1},
                    {u'attr_b': 2.1, u'attr_c': u'bb'},
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
            ptr.data.TableData(
                table_name=u'testsheet1',
                header_list=[u'a1', u'b1', u'c1'],
                record_list=[
                    [u'aa1', u'ab1', u'ac1'],
                    [1.0, 1.1, u'a'],
                    [2.0, 2.2, u'bb'],
                    [3.0, 3.3, u'cc'],
                ]),
            ptr.data.TableData(
                table_name=u'testsheet3',
                header_list=[u'a3', u'b3', u'c3'],
                record_list=[
                    [u'aa3', u'ab3', u'ac3'],
                    [4.0, 1.1, u'a'],
                    [5.0, u'', u'bb'],
                    [6.0, 3.3, u''],
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
