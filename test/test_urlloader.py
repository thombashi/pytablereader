# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function

import pytest
import responses

import pytablereader as ptr


class Test_TableUrlLoader_constructor:

    @responses.activate
    @pytest.mark.parametrize(["value", "format_name", "expected"], [
        [
            "https://raw.githubusercontent.com/valid/test/data/validext.csv",
            None, ptr.CsvTableTextLoader
        ],
        [
            "https://raw.githubusercontent.com/valid/test/data/validext.csv/",
            None, ptr.CsvTableTextLoader
        ],
        [
            "https://raw.githubusercontent.com/valid/test/data/validext.xlsx",
            None, ptr.ExcelTableFileLoader
        ],
        [
            "https://raw.githubusercontent.com/valid/test/data/validext.html",
            None, ptr.HtmlTableTextLoader
        ],
        [
            "https://raw.githubusercontent.com/valid/test/data/validext.htm/",
            None, ptr.HtmlTableTextLoader
        ],
        [
            "https://raw.githubusercontent.com/valid/test/data/validext.json",
            None, ptr.JsonTableTextLoader
        ],
        [
            "https://github.com/validext.md",
            None, ptr.MarkdownTableTextLoader
        ],
        ["https://github.com/validext.txt", "csv", ptr.CsvTableTextLoader],
        ["https://github.com/validext.txt", "html", ptr.HtmlTableTextLoader],
        ["https://github.com/validext.txt", "json", ptr.JsonTableTextLoader],
        [
            "https://github.com/invalidext.txt",
            "markdown", ptr.MarkdownTableTextLoader
        ],
        [
            "https://github.com/invalidext.txt",
            "mediawiki", ptr.MediaWikiTableTextLoader
        ],
    ])
    def test_normal(self, value, format_name, expected):
        responses.add(
            responses.GET,
            value,
            body='''{}''',
            content_type='text/plain; charset=utf-8',
            status=200
        )

        loader = ptr.TableUrlLoader(value, format_name)
        expected_loader = expected("")

        assert loader.source_type == expected_loader.source_type
        assert loader.format_name == expected_loader.format_name

    @responses.activate
    @pytest.mark.parametrize(["value", "format_name", "expected"], [
        [None, None, ptr.InvalidUrlError],
        ["", None, ptr.InvalidUrlError],
        ["https://github.com/", None, ptr.InvalidUrlError],
        [
            "https://raw.githubusercontent.com/invalid/test/data/invalidext.txt",
            None, ptr.LoaderNotFoundError
        ],
        [
            "https://raw.githubusercontent.com/invalid/test/data/notexist.json",
            None, ptr.HTTPError
        ],
        [
            "https://raw.githubusercontent.com/invalid/test/data/invalidext.txt",
            "invalidformat", ptr.LoaderNotFoundError
        ],
    ])
    def test_exception(self, value, format_name, expected):
        responses.add(
            responses.GET,
            value,
            body='''404: Not Found''',
            status=404,
        )

        with pytest.raises(expected):
            ptr.TableUrlLoader(value, format_name)


class Test_TableUrlLoader_load:

    @responses.activate
    def test_normal_csv(self):
        url = 'https://raw.githubusercontent.com/valid/test/data/validdata.csv'
        responses.add(
            responses.GET,
            url,
            body='''"attr_a","attr_b","attr_c"
    1,4,"a"
    2,2.1,"bb"
    3,120.9,"ccc"''',
            content_type='text/plain; charset=utf-8',
            status=200
        )

        expeced_list = [
            ptr.TableData(
                "csv1",
                ["attr_a", "attr_b", "attr_c"],
                [
                    [1, 4,      "a"],
                    [2, "2.1",    "bb"],
                    [3, "120.9",  "ccc"],
                ])
        ]

        loader = ptr.TableUrlLoader(url)
        for tabledata, expected in zip(loader.load(), expeced_list):
            # print(tabledata.dumps())
            # print(expected.dumps())
            assert tabledata == expected

    @responses.activate
    def test_normal_json(self):
        url = 'https://raw.githubusercontent.com/valid/test/data/validdata.json'
        responses.add(
            responses.GET,
            url,
            body='''[
        {"attr_a": 1},
        {"attr_b": 2.1, "attr_c": "bb"}
    ]''',
            content_type='text/plain; charset=utf-8',
            status=200
        )

        expeced_list = [
            ptr.TableData(
                "json1",
                ["attr_a", "attr_b", "attr_c"],
                [
                    {u'attr_a': 1},
                    {u'attr_b': 2.1, u'attr_c': u'bb'},
                ]
            )
        ]

        loader = ptr.TableUrlLoader(url)
        for tabledata, expected in zip(loader.load(), expeced_list):
            assert tabledata == expected


"""
@responses.activate
def test_timeline():
    url = 'https://github.com/timeline.json'
    responses.add(
        responses.GET,
        url,
        body='{"message":"Hello there, wayfaring stranger. If you’re reading this then you probably didn’t see our blog post a couple of years back announcing that this API would go away: http://git.io/17AROg Fear not, you should be able to get what you need from the shiny new Events API instead.","documentation_url":"https://developer.github.com/v3/activity/events/#list-public-events"}',
        content_type='application/json; charset=utf-8',
        status=410
    )

    loader = ptr.TableUrlLoader(url)
"""
