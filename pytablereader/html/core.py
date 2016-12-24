# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import io

from .._constant import (
    SourceType,
    TableNameTemplate as tnt
)
from .._logger import logger
from .._validator import (
    FileValidator,
    TextValidator
)
from ..interface import TableLoader
from .formatter import HtmlTableFormatter


class HtmlTableLoader(TableLoader):
    """
    Abstract class of HTML table loader.
    """

    @property
    def format_name(self):
        return "html"

    def _get_default_table_name_template(self):
        return "{:s}_{:s}".format(tnt.TITLE, tnt.KEY)


class HtmlTableFileLoader(HtmlTableLoader):
    """
    HTML format file loader class.

    :param str file_path: Path to the loading HTML file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(title)s_%(key)s``.

    .. py:attribute:: encoding

        HTML file encoding. Defaults to ``"utf-8"``.
    """

    def __init__(self, file_path=None):
        super(HtmlTableFileLoader, self).__init__(file_path)

        self.encoding = "utf-8"

        self._validator = FileValidator(file_path)

    def load(self):
        """
        Extract tabular data as |TableData| incetances from HTML table tags in
        a HTML file.
        |load_source_desc_file|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            format specifier     value after the replacement
            ===================  ==============================================
            ``%(filename)s``     |filename_desc|
            ``%(title)s``        Title tag text of the html.
            ``%(key)s``          | This is replaced to :
                                 | **(1)** ``id`` attribute of the table tag
                                 | **(2)** ``%(format_name)s%(format_id)s``
                                 | if ``id`` attribute is not included
                                 | in the table tag.
            ``%(format_name)s``  ``"html"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the HTML data is invalid or empty.

        .. note::

            Table tag attributes are ignored with loaded |TableData|.
        """

        self._validate()

        logger.debug("\n".join([
            "loading html file:",
            "  path={}".format(self.source),
            "  encoding={}".format(self.encoding),
        ]))

        formatter = None
        with io.open(self.source, "r", encoding=self.encoding) as fp:
            formatter = HtmlTableFormatter(fp.read())
        formatter.accept(self)

        return formatter.to_table_data()


class HtmlTableTextLoader(HtmlTableLoader):
    """
    HTML format text loader class.

    :param str text: HTML text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(title)s_%(key)s``.
    """

    def __init__(self, text):
        super(HtmlTableTextLoader, self).__init__(text)

        self._validator = TextValidator(text)

    def load(self):
        """
        Extract tabular data as |TableData| incetances from HTML table tags in
        a HTML text object.
        |load_source_desc_text|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            format specifier     value after the replacement
            ===================  ==============================================
            ``%(filename)s``     ``""``
            ``%(title)s``        Title tag text of the html.
            ``%(key)s``          | This is replaced to :
                                 | **(1)** ``id`` attribute of the table tag
                                 | **(2)** ``%(format_name)s%(format_id)s``
                                 | if ``id`` attribute is not included
                                 | in the table tag.
            ``%(format_name)s``  ``"html"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the HTML data is invalid or empty.
        """

        self._validate()

        logger.debug("\n".join([
            "loading html text",
        ]))

        formatter = HtmlTableFormatter(self.source)
        formatter.accept(self)

        return formatter.to_table_data()
