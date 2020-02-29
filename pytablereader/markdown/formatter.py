"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import typepy

from pytablereader import DataError

from ..html.formatter import HtmlTableFormatter


class MarkdownTableFormatter(HtmlTableFormatter):
    def __init__(self, source_data, logger=None):
        import markdown

        if typepy.is_null_string(source_data):
            raise DataError

        super().__init__(
            markdown.markdown(source_data, extensions=["markdown.extensions.tables"]), logger=logger
        )
