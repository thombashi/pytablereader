# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ..html.formatter import HtmlTableFormatter


class MediaWikiTableFormatter(HtmlTableFormatter):

    def __init__(self, source_data):
        import pypandoc

        super(MediaWikiTableFormatter, self).__init__(
            pypandoc.convert_text(source_data, "html", format="mediawiki"))
