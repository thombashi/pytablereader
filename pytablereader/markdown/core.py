"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from .._common import get_file_encoding
from .._constant import SourceType
from .._constant import TableNameTemplate as tnt
from .._logger import FileSourceLogger, TextSourceLogger
from .._validator import FileValidator, TextValidator
from ..interface import AbstractTableReader
from .formatter import MarkdownTableFormatter


class MarkdownTableLoader(AbstractTableReader):
    """
    The abstract class of Markdown table loaders.
    """

    @property
    def format_name(self):
        return "markdown"


class MarkdownTableFileLoader(MarkdownTableLoader):
    """
    A file loader class to extract tabular data from Markdown files.

    :param str file_path: Path to the loading Markdown file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s_%(key)s``.
    """

    def __init__(self, file_path=None, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(file_path, quoting_flags, type_hints, type_hint_rules)

        self.encoding = None

        self._validator = FileValidator(file_path)
        self._logger = FileSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a Markdown file.
        |load_source_desc_file|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            Format specifier     Value after the replacement
            ===================  ==============================================
            ``%(filename)s``     |filename_desc|
            ``%(key)s``          ``%(format_name)s%(format_id)s``
            ``%(format_name)s``  ``"markdown"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.DataError:
            If the Markdown data is invalid or empty.
        """

        self._validate()
        self._logger.logging_load()
        self.encoding = get_file_encoding(self.source, self.encoding)

        with open(self.source, encoding=self.encoding) as fp:
            formatter = MarkdownTableFormatter(fp.read(), self._logger)
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return f"{tnt.FILENAME:s}_{tnt.KEY:s}"


class MarkdownTableTextLoader(MarkdownTableLoader):
    """
    A text loader class to extract tabular data from Markdown text data.

    :param str text: Markdown text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(key)s``.
    """

    @property
    def source_type(self):
        return SourceType.TEXT

    def __init__(self, text=None, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(text, quoting_flags, type_hints)

        self._validator = TextValidator(text)
        self._logger = TextSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a Markdown text
        object.
        |load_source_desc_text|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            Format specifier     Value after the replacement
            ===================  ==============================================
            ``%(filename)s``     ``""``
            ``%(key)s``          ``%(format_name)s%(format_id)s``
            ``%(format_name)s``  ``"markdown"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.DataError:
            If the Markdown data is invalid or empty.
        """

        self._validate()
        self._logger.logging_load()

        formatter = MarkdownTableFormatter(self.source, self._logger)
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return f"{tnt.KEY:s}"
