# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty

from ..error import LoaderNotFoundError
from ..factory import TableFileLoaderFactory
from ._base import TableLoaderManager


class TableFileLoader(TableLoaderManager):
    """
    Loader class to loading tables from a file.

    :param str file_path: Path to the file to load.
    :param str format_name: Data format name to load.
        Supported formats are:
            * ``"csv"``
            * ``"excel"``
            * ``"html"``
            * ``"json"``
            * ``"markdown"``
            * ``"mediawiki"``
    :raise pytablereader.InvalidFilePathError:
        If ``file_path`` is a invalid file path.
    :raises pytablereader.LoaderNotFoundError:
        If appropriate loader not found to loading the file.
    """

    def __init__(self, file_path, format_name=None):
        loader_factory = TableFileLoaderFactory(file_path)

        if dataproperty.is_not_empty_string(format_name):
            loader = loader_factory.create_from_format_name(format_name)
        else:
            loader = loader_factory.create_from_path()

        super(TableFileLoader, self).__init__(loader)

    def load(self):
        """
        Loading table data from a file as ``format_name`` format.
        Automatically detect file format if ``format_name`` is |None|.

        :return: Loaded table data iterator.
        :rtype: |TableData| iterator

        .. seealso::

            * :py:meth:`pytablereader.factory.TableFileLoaderFactory.create_from_format_name`
            * :py:meth:`pytablereader.factory.TableFileLoaderFactory.create_from_path`
        """

        return super(TableFileLoader, self).load()
