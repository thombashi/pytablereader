# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

import pytablereader as ptr


class Test_TableUrlLoader_constructor:

    @pytest.mark.parametrize(["value", "format_name", "expected"], [
        [
            "https://github.com/thombashi/sandbox/blob/master/data/valid.csv",
            None, ptr.CsvTableTextLoader
        ],
        [
            "https://github.com/thombashi/sandbox/blob/master/data/valid.csv/",
            None, ptr.CsvTableTextLoader
        ],
        [
            "https://github.com/thombashi/sandbox/blob/master/data/valid.xlsx",
            None, ptr.ExcelTableFileLoader
        ],
        [
            "https://github.com/thombashi/sandbox/blob/master/data/valid.html",
            None, ptr.HtmlTableTextLoader
        ],
        [
            "https://github.com/thombashi/sandbox/blob/master/data/valid.htm/",
            None, ptr.HtmlTableTextLoader
        ],
        [
            "https://github.com/thombashi/sandbox/blob/master/data/valid.json",
            None, ptr.JsonTableTextLoader
        ],
        [
            "https://github.com/valid.md",
            None, ptr.MarkdownTableTextLoader
        ],
        ["https://github.com/valid.txt", "csv", ptr.CsvTableTextLoader],
        ["https://github.com/valid.txt", "html", ptr.HtmlTableTextLoader],
        ["https://github.com/valid.txt", "json", ptr.JsonTableTextLoader],
        [
            "https://github.com/valid.txt",
            "markdown", ptr.MarkdownTableTextLoader
        ],
        [
            "https://github.com/valid.txt",
            "mediawiki", ptr.MediaWikiTableTextLoader
        ],
    ])
    def test_normal(self, value, format_name, expected):
        loader = ptr.TableUrlLoader(value, format_name)
        expected_loader = expected("")

        assert loader.source_type == expected_loader.source_type
        assert loader._format_name == expected_loader._format_name

    @pytest.mark.parametrize(["value", "format_name", "expected"], [
        [None, None, ptr.InvalidUrlError],
        ["", None, ptr.InvalidUrlError],
        ["https://github.com/", None, ptr.InvalidUrlError],
        [
            "https://github.com/thombashi/sandbox/blob/master/data/invalid.txt",
            None, ptr.LoaderNotFoundError
        ],
        [
            "https://github.com/thombashi/sandbox/blob/master/data/invalid.txt",
            "invalidformat", ptr.LoaderNotFoundError
        ],
    ])
    def test_exception(self, value, format_name, expected):
        with pytest.raises(expected):
            ptr.TableUrlLoader(value, format_name)
