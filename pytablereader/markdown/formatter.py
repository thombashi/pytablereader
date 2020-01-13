# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import typepy

from pytablereader import DataError

from ..html.formatter import HtmlTableFormatter


class MarkdownTableFormatter(HtmlTableFormatter):
    def __init__(self, source_data, logger=None):
        import markdown

        if typepy.is_null_string(source_data):
            raise DataError

        super(MarkdownTableFormatter, self).__init__(
            markdown.markdown(source_data, extensions=["markdown.extensions.tables"]), logger=logger
        )
