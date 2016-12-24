# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from .._constant import (
    SourceType,
    TableNameTemplate as tnt
)
from .._validator import (
    FileValidator,
    TextValidator
)
from ..interface import TableLoader
from .formatter import MarkdownTableFormatter


class MarkdownTableLoader(TableLoader):
    """
    Abstract class of Markdown table loader.
    """

    @property
    def format_name(self):
        return "markdown"


class MarkdownTableFileLoader(MarkdownTableLoader):
    """
    Markdown format file loader class.

    :param str file_path: Path to the loading Markdown file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s_%(key)s``.
    """

    def __init__(self, file_path=None):
        super(MarkdownTableFileLoader, self).__init__(file_path)

        self._validator = FileValidator(file_path)

    def load(self):
        """
        Extract tabular data as |TableData| incetances from a Markdown file.
        |load_source_desc_file|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            format specifier     value after the replacement
            ===================  ==============================================
            ``%(filename)s``     |filename_desc|
            ``%(key)s``          ``%(format_name)s%(format_id)s``
            ``%(format_name)s``  ``"markdown"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the Markdown data is invalid or empty.
        """

        self._validate()

        formatter = None
        with open(self.source, "r") as fp:
            formatter = MarkdownTableFormatter(fp.read())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}_{:s}".format(tnt.FILENAME, tnt.KEY)


class MarkdownTableTextLoader(MarkdownTableLoader):
    """
    Markdown format text loader class.

    :param str text: Markdown text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(key)s``.
    """

    @property
    def source_type(self):
        return SourceType.TEXT

    def __init__(self, text):
        super(MarkdownTableTextLoader, self).__init__(text)

        self._validator = TextValidator(text)

    def load(self):
        """
        Extract tabular data as |TableData| incetances from a Markdown text object.
        |load_source_desc_text|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            format specifier     value after the replacement
            ===================  ==============================================
            ``%(filename)s``     ``""``
            ``%(key)s``          ``%(format_name)s%(format_id)s``
            ``%(format_name)s``  ``"markdown"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the Markdown data is invalid or empty.
        """

        self._validate()

        formatter = MarkdownTableFormatter(self.source)
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}".format(tnt.KEY)
