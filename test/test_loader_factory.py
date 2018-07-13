# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import pytablereader as ptr
import pytest


class Test_TableFileLoaderFactory(object):
    @pytest.mark.parametrize(["value", "expected"], [[None, ValueError]])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            ptr.factory.TableFileLoaderFactory(value)


class Test_TableFileLoaderFactory_create_from_path(object):
    @pytest.mark.parametrize(
        ["value", "extension", "expected"],
        [
            ["valid_ext.csv", "csv", ptr.CsvTableFileLoader],
            ["valid_ext.CSV", "csv", ptr.CsvTableFileLoader],
            ["valid_ext.html", "html", ptr.HtmlTableFileLoader],
            ["valid_ext.HTML", "html", ptr.HtmlTableFileLoader],
            ["valid_ext.htm", "htm", ptr.HtmlTableFileLoader],
            ["valid_ext.HTM", "htm", ptr.HtmlTableFileLoader],
            ["valid_ext.json", "json", ptr.JsonTableFileLoader],
            ["valid_ext.JSON", "json", ptr.JsonTableFileLoader],
            ["valid_ext.md", "md", ptr.MarkdownTableFileLoader],
            ["valid_ext.MD", "md", ptr.MarkdownTableFileLoader],
            ["valid_ext.sqlite", "sqlite", ptr.SqliteFileLoader],
            ["valid_ext.sqlite3", "sqlite3", ptr.SqliteFileLoader],
            ["valid_ext.tsv", "tsv", ptr.TsvTableFileLoader],
            ["valid_ext.TSV", "tsv", ptr.TsvTableFileLoader],
            ["valid_ext.xls", "xls", ptr.ExcelTableFileLoader],
            ["valid_ext.XLS", "xls", ptr.ExcelTableFileLoader],
            ["valid_ext.xlsx", "xlsx", ptr.ExcelTableFileLoader],
            ["valid_ext.XLSX", "xlsx", ptr.ExcelTableFileLoader],
        ],
    )
    def test_normal(self, value, extension, expected):
        loader_factory = ptr.factory.TableFileLoaderFactory(value)
        loader = loader_factory.create_from_path()

        assert loader_factory.file_extension.lower() == extension
        assert loader.source == value
        assert isinstance(loader, expected)

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["hoge", ptr.LoaderNotFoundError],
            ["hoge.txt", ptr.LoaderNotFoundError],
            [".txt", ptr.LoaderNotFoundError],
            ["", ptr.InvalidFilePathError],
        ],
    )
    def test_exception(self, value, expected):
        loader_factory = ptr.factory.TableFileLoaderFactory(value)

        with pytest.raises(expected):
            loader_factory.create_from_path()


class Test_TableFileLoaderFactory_create_from_format_name(object):
    @pytest.mark.parametrize(
        ["file_path", "format_name", "expected"],
        [
            ["valid_ext.html", "csv", ptr.CsvTableFileLoader],
            ["invalid_ext.txt", "CSV", ptr.CsvTableFileLoader],
            ["valid_ext.html", "excel", ptr.ExcelTableFileLoader],
            ["invalid_ext.txt", "Excel", ptr.ExcelTableFileLoader],
            ["valid_ext.json", "html", ptr.HtmlTableFileLoader],
            ["invalid_ext.txt", "HTML", ptr.HtmlTableFileLoader],
            ["valid_ext.html", "json", ptr.JsonTableFileLoader],
            ["invalid_ext.txt", "JSON", ptr.JsonTableFileLoader],
            ["valid_ext.html", "markdown", ptr.MarkdownTableFileLoader],
            ["invalid_ext.txt", "Markdown", ptr.MarkdownTableFileLoader],
            ["valid_ext.html", "mediawiki", ptr.MediaWikiTableFileLoader],
            ["invalid_ext.txt", "MediaWiki", ptr.MediaWikiTableFileLoader],
            ["valid_ext.db", "sqlite", ptr.SqliteFileLoader],
            ["valid_ext.html", "tsv", ptr.TsvTableFileLoader],
            ["invalid_ext.txt", "TSV", ptr.TsvTableFileLoader],
        ],
    )
    def test_normal(self, file_path, format_name, expected):
        loader_factory = ptr.factory.TableFileLoaderFactory(file_path)
        loader = loader_factory.create_from_format_name(format_name)

        assert loader.source == file_path
        assert isinstance(loader, expected)

    @pytest.mark.parametrize(
        ["file_path", "format_name", "expected"],
        [
            ["valid_ext.csv", "not_exist_format", ptr.LoaderNotFoundError],
            ["valid_ext.csv", "", ptr.LoaderNotFoundError],
            ["valid_ext.csv", None, TypeError],
            ["valid_ext.csv", 0, TypeError],
            ["valid_ext.csv", "auto", ptr.LoaderNotFoundError],
        ],
    )
    def test_exception(self, file_path, format_name, expected):
        loader_factory = ptr.factory.TableFileLoaderFactory(file_path)

        with pytest.raises(expected):
            loader_factory.create_from_format_name(format_name)
