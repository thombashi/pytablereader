"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

import pytablereader as ptr


class Test_TableTextLoaderFactory:
    @pytest.mark.parametrize(["value", "expected"], [[None, ValueError]])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            ptr.factory.TableTextLoaderFactory(value)


class Test_TableTextLoaderFactory_create_from_format_name:
    @pytest.mark.parametrize(
        ["format_name", "expected"],
        [
            ["csv", ptr.CsvTableTextLoader],
            ["CSV", ptr.CsvTableTextLoader],
            ["html", ptr.HtmlTableTextLoader],
            ["HTML", ptr.HtmlTableTextLoader],
            ["json", ptr.JsonTableTextLoader],
            ["JSON", ptr.JsonTableTextLoader],
            ["markdown", ptr.MarkdownTableTextLoader],
            ["Markdown", ptr.MarkdownTableTextLoader],
            ["mediawiki", ptr.MediaWikiTableTextLoader],
            ["MediaWiki", ptr.MediaWikiTableTextLoader],
            ["tsv", ptr.TsvTableTextLoader],
            ["TSV", ptr.TsvTableTextLoader],
        ],
    )
    def test_normal(self, format_name, expected):
        loader_factory = ptr.factory.TableTextLoaderFactory("dummy")
        loader = loader_factory.create_from_format_name(format_name)

        assert isinstance(loader, expected)

    @pytest.mark.parametrize(
        ["format_name", "expected"],
        [
            ["not_exist_format", ptr.LoaderNotFoundError],
            ["", ptr.LoaderNotFoundError],
            [None, TypeError],
            [0, TypeError],
            ["auto", ptr.LoaderNotFoundError],
        ],
    )
    def test_exception(self, format_name, expected):
        loader_factory = ptr.factory.TableTextLoaderFactory("dummyy")

        with pytest.raises(expected):
            loader_factory.create_from_format_name(format_name)
