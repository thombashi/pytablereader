# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pypandoc

from .._constant import TableNameTemplate as tnt
from ..data import TableData
from ..html.formatter import HtmlTableFormatter


class MediaWikiTableFormatter(HtmlTableFormatter):

    def __init__(self, source_data):
        super(MediaWikiTableFormatter, self).__init__(
            pypandoc.convert_text(source_data, "html", format="mediawiki"))
