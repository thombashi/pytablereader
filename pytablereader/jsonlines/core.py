# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import abc
import io
from collections import OrderedDict

import simplejson as json
import six
from simplejson import JSONDecodeError

from .._common import get_file_encoding
from .._constant import SourceType
from .._constant import TableNameTemplate as tnt
from .._logger import FileSourceLogger, TextSourceLogger
from .._validator import FileValidator, TextValidator
from ..error import ValidationError
from ..interface import TableLoader
from .formatter import JsonLinesTableFormatter


@six.add_metaclass(abc.ABCMeta)
class JsonLinesTableLoader(TableLoader):
    """
    An abstract class of JSON table loaders.
    """

    @property
    def format_name(self):
        return "json_lines"

    @abc.abstractmethod
    def load_dict(self):  # pragma: no cover
        pass


class JsonLinesTableFileLoader(JsonLinesTableLoader):
    """
    A file loader class to extract tabular data from Line-delimited JSON files.

    :param str file_path: Path to the loading Line-delimited JSON file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s_%(key)s``.
    """

    def __init__(self, file_path=None, quoting_flags=None):
        super(JsonLinesTableFileLoader, self).__init__(file_path, quoting_flags)

        self.encoding = None

        self._validator = FileValidator(file_path)
        self._logger = FileSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a Line-delimited JSON file.
        |load_source_desc_file|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

        :rtype: |TableData| iterator
        :raises pytablereader.DataError:
            If the data is invalid Line-delimited JSON.
        :raises pytablereader.error.ValidationError:
            If the data is not acceptable Line-delimited JSON format.
        """

        formatter = JsonLinesTableFormatter(self.load_dict())
        formatter.accept(self)

        return formatter.to_table_data()

    def load_dict(self):
        self._validate()
        self._logger.logging_load()
        self.encoding = get_file_encoding(self.source, self.encoding)

        buffer = []
        with io.open(self.source, "r", encoding=self.encoding) as fp:
            for line in fp.readlines():
                try:
                    buffer.append(json.loads(line, object_pairs_hook=OrderedDict))
                except JSONDecodeError as e:
                    raise ValidationError(e)

        return buffer

    def _get_default_table_name_template(self):
        return "{:s}_{:s}".format(tnt.FILENAME, tnt.KEY)


class JsonLinesTableTextLoader(JsonLinesTableLoader):
    """
    A text loader class to extract tabular data from Line-delimited JSON text data.

    :param str text: Line-delimited JSON text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(key)s``.
    """

    @property
    def source_type(self):
        return SourceType.TEXT

    def __init__(self, text, quoting_flags=None):
        super(JsonLinesTableTextLoader, self).__init__(text, quoting_flags)

        self._validator = TextValidator(text)
        self._logger = TextSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a Line-delimited JSON text object.
        |load_source_desc_text|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

        :rtype: |TableData| iterator

        .. seealso::

            :py:meth:`.JsonLinesTableFileLoader.load()`
        """

        formatter = JsonLinesTableFormatter(self.load_dict())
        formatter.accept(self)

        return formatter.to_table_data()

    def load_dict(self):
        self._validate()
        self._logger.logging_load()

        buffer = []
        for line in self.source.splitlines():
            try:
                buffer.append(json.loads(line, object_pairs_hook=OrderedDict))
            except JSONDecodeError as e:
                raise ValidationError(e)

        return buffer

    def _get_default_table_name_template(self):
        return "{:s}".format(tnt.KEY)
