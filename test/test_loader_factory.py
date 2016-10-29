# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

import pytablereader as ptr


class Test_FileLoaderFactory_constructor:

    @pytest.mark.parametrize(["value", "expected"], [
        [None, ptr.InvalidFilePathError],
        ["", ptr.InvalidFilePathError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            ptr.FileLoaderFactory(value)


class Test_FileLoaderFactory_create_from_file_path:

    @pytest.mark.parametrize(["value", "extension", "expected"], [
        ["testfile.csv", "csv", ptr.CsvTableFileLoader],
        ["testfile.html", "html", ptr.HtmlTableFileLoader],
        ["testfile.htm", "htm", ptr.HtmlTableFileLoader],
        ["testfile.json", "json", ptr.JsonTableFileLoader],
        ["testfile.md", "md", ptr.MarkdownTableFileLoader],
        ["testfile.xls", "xls", ptr.ExcelTableFileLoader],
        ["testfile.xlsx", "xlsx", ptr.ExcelTableFileLoader],
    ])
    def test_normal(self, value, extension, expected):
        loader_factory = ptr.FileLoaderFactory(value)
        loader = loader_factory.create_from_file_path()

        assert loader_factory.file_extension == extension
        assert loader.source == value
        assert isinstance(loader, expected)

    @pytest.mark.parametrize(["value", "expected"], [
        ["hoge", ptr.LoaderNotFoundError],
        ["hoge.txt", ptr.LoaderNotFoundError],
        [".txt", ptr.LoaderNotFoundError],
    ])
    def test_exception(self, value, expected):
        loader_factory = ptr.FileLoaderFactory(value)

        with pytest.raises(expected):
            loader_factory.create_from_file_path()


class Test_FileLoaderFactory_create_from_format_name:

    @pytest.mark.parametrize(["value", "format_name", "expected"], [
        ["testfile.html", "csv", ptr.CsvTableFileLoader],
        ["testfile.html", "excel", ptr.ExcelTableFileLoader],
        ["testfile.json", "html", ptr.HtmlTableFileLoader],
        ["testfile.html", "json", ptr.JsonTableFileLoader],
        ["testfile.html", "markdown", ptr.MarkdownTableFileLoader],
        ["testfile.html", "mediawiki", ptr.MediaWikiTableFileLoader],
        ["testfile.html", "json", ptr.JsonTableFileLoader],
        ["testfile.html", "auto", ptr.HtmlTableFileLoader],
    ])
    def test_normal(self, value, format_name, expected):
        loader_factory = ptr.FileLoaderFactory(value)
        loader = loader_factory.create_from_format_name(format_name)

        assert loader.source == value
        assert isinstance(loader, expected)
