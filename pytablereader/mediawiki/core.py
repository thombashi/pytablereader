# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from .._constant import SourceType
from .._constant import TableNameTemplate as tnt
from ..interface import TableLoader
from .formatter import MediaWikiTableFormatter


class MediaWikiTableLoader(TableLoader):
    """
    Abstract class of MediaWiki table loader.
    """

    @property
    def _format_name(self):
        return "mediawiki"


class MediaWikiTableFileLoader(MediaWikiTableLoader):
    """
    Concrete class of MediaWiki file loader.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s_%(key)s``.
    """

    @property
    def source_type(self):
        return SourceType.FILE

    def __init__(self, file_path=None):
        super(MediaWikiTableFileLoader, self).__init__(file_path)

    def load(self):
        """
        Extract |TableData| from MediaWiki tables in a MediaWiki file.
        |load_source_desc_file|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            format specifier     value after the replacement
            ===================  ==============================================
            ``%(filename)s``     |filename_desc|
            ``%(key)s``          | This is replaced to :
                                 | **(1)** ``caption`` mark of the table
                                 | **(2)** ``%(format_name)s%(format_id)s``
                                 | if ``caption`` mark not included
                                 | in the table.
            ``%(format_name)s``  ``"mediawiki"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the MediaWiki data is invalid or empty.
        """

        self._validate()

        formatter = None
        with open(self.source, "r") as fp:
            formatter = MediaWikiTableFormatter(fp.read())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}_{:s}".format(tnt.FILENAME, tnt.KEY)


class MediaWikiTableTextLoader(MediaWikiTableLoader):
    """
    Concrete class of MediaWiki text loader.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(key)s``.
    """

    @property
    def source_type(self):
        return SourceType.TEXT

    def __init__(self, text):
        super(MediaWikiTableTextLoader, self).__init__(text)

    def load(self):
        """
        Extract |TableData| from MediaWiki tables in a MediaWiki text.
        |load_source_desc_text|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            format specifier     value after the replacement
            ===================  ==============================================
            ``%(filename)s``     ``""``
            ``%(key)s``          | This is replaced to :
                                 | **(1)** ``caption`` mark of the table
                                 | **(2)** ``%(format_name)s%(format_id)s``
                                 | if ``caption`` mark not included
                                 | in the table.
            ``%(format_name)s``  ``"mediawiki"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.error.InvalidDataError:
            If the MediaWiki data is invalid or empty.
        """

        self._validate()

        formatter = MediaWikiTableFormatter(self.source)
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}".format(tnt.KEY)
