"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from .._common import get_file_encoding
from .._constant import TableNameTemplate as tnt
from .._logger import FileSourceLogger, TextSourceLogger
from .._validator import FileValidator, TextValidator
from ..interface import AbstractTableReader
from .formatter import HtmlTableFormatter


class HtmlTableLoader(AbstractTableReader):
    """
    An abstract class of HTML table loaders.
    """

    @property
    def format_name(self):
        return "html"

    def _get_default_table_name_template(self):
        return f"{tnt.TITLE:s}_{tnt.KEY:s}"


class HtmlTableFileLoader(HtmlTableLoader):
    """
    A file loader class to extract tabular data from HTML files.

    :param str file_path: Path to the loading HTML file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(title)s_%(key)s``.

    .. py:attribute:: encoding

        HTML file encoding. Defaults to ``"utf-8"``.
    """

    def __init__(self, file_path=None, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(file_path, quoting_flags, type_hints, type_hint_rules)

        self.encoding = None

        self._validator = FileValidator(file_path)
        self._logger = FileSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from HTML table tags in
        a HTML file.
        |load_source_desc_file|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            Format specifier     Value after the replacement
            ===================  ==============================================
            ``%(filename)s``     |filename_desc|
            ``%(title)s``        ``<title>`` tag value of the HTML.
            ``%(key)s``          | This replaced to:
                                 | **(1)** ``id`` attribute of the table tag
                                 | **(2)** ``%(format_name)s%(format_id)s``
                                 | if ``id`` attribute not present in the
                                 | table tag.
            ``%(format_name)s``  ``"html"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.DataError:
            If the HTML data is invalid or empty.

        .. note::

            Table tag attributes ignored with loaded |TableData|.
        """

        self._validate()
        self._logger.logging_load()
        self.encoding = get_file_encoding(self.source, self.encoding)

        with open(self.source, encoding=self.encoding) as fp:
            formatter = HtmlTableFormatter(fp.read(), self._logger)
        formatter.accept(self)

        return formatter.to_table_data()


class HtmlTableTextLoader(HtmlTableLoader):
    """
    A text loader class to extract tabular data from HTML text data.

    :param str text: HTML text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(title)s_%(key)s``.
    """

    def __init__(self, text, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(text, quoting_flags, type_hints, type_hint_rules)

        self._validator = TextValidator(text)
        self._logger = TextSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from HTML table tags in
        a HTML text object.
        |load_source_desc_text|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            Format specifier     Value after the replacement
            ===================  ==============================================
            ``%(filename)s``     ``""``
            ``%(title)s``        ``<title>`` tag value of the HTML.
            ``%(key)s``          | This replaced to:
                                 | **(1)** ``id`` attribute of the table tag
                                 | **(2)** ``%(format_name)s%(format_id)s``
                                 | if ``id`` attribute is not included
                                 | in the table tag.
            ``%(format_name)s``  ``"html"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.DataError:
            If the HTML data is invalid or empty.
        """

        self._validate()
        self._logger.logging_load()

        formatter = HtmlTableFormatter(self.source, self._logger)
        formatter.accept(self)

        return formatter.to_table_data()
