# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import abc
import threading

import dataproperty
import path
import six

from ._constant import (
    SourceType,
    TableNameTemplate as tnt
)
from .error import InvalidTableNameError


@six.add_metaclass(abc.ABCMeta)
class TableLoaderInterface(object):
    """
    Interface class of table loader class.
    """

    @abc.abstractproperty
    def format_name(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def source_type(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def load(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def inc_table_count(self):  # pragma: no cover
        pass


class TableLoader(TableLoaderInterface):
    """
    Abstract class of table data file loader.

    .. py:attribute:: table_name

        Table name string.

    .. py:attribute:: source

        Table data source to load.
    """

    __table_count_lock = threading.Lock()
    __global_table_count = 0
    __format_table_count = {}

    @property
    def source_type(self):
        return self._validator.source_type

    def __init__(self, source):
        self.table_name = tnt.DEFAULT
        self.source = source
        self._validator = None

    def get_format_key(self):
        return "{:s}{:d}".format(
            self.format_name,
            self.__get_format_table_count())

    def make_table_name(self):
        return self._make_table_name()

    def inc_table_count(self):
        with self.__table_count_lock:
            self.__global_table_count += 1
            self.__format_table_count[self.format_name] = (
                self.__get_format_table_count() + 1)

    @abc.abstractmethod
    def _get_default_table_name_template(self):  # pragma: no cover
        pass

    def _validate(self):
        self._validate_table_name()
        self._validate_source()

    def _validate_table_name(self):
        try:
            if dataproperty.is_empty_string(self.table_name):
                raise ValueError("table name is empty")
        except (TypeError, AttributeError):
            raise TypeError("table_name must be a string")

    def _validate_source(self):
        self._validator.validate()

    def __get_format_table_count(self):
        return self.__format_table_count.get(self.format_name, 0)

    def _get_filename_tablename_mapping(self):
        filename = ""
        if all([
            self.source_type == SourceType.FILE,
            dataproperty.is_not_empty_string(self.source),
        ]):
            filename = path.Path(self.source).namebase

        return (tnt.FILENAME, filename)

    def _get_basic_tablename_mapping(self):
        return [
            (tnt.DEFAULT, self._get_default_table_name_template()),
            (tnt.FORMAT_NAME, self.format_name),
            (tnt.FORMAT_ID, str(self.__get_format_table_count())),
            (tnt.GLOBAL_ID, str(self.__global_table_count)),
            self._get_filename_tablename_mapping(),
        ]

    def _replace_table_name_template(self, table_name_mapping):
        self._validate_table_name()

        table_name = self.table_name
        for teamplate, value in table_name_mapping:
            table_name = table_name.replace(teamplate, value)

        return self._sanitize_table_name(table_name)

    def _make_table_name(self):
        self._validate_table_name()

        return self._replace_table_name_template(
            self._get_basic_tablename_mapping())

    def _sanitize_table_name(self, table_name):
        if dataproperty.is_empty_string(table_name):
            raise InvalidTableNameError(
                "table name is empty after the template replacement")

        return table_name.strip("_")

    @classmethod
    def clear_table_count(cls):
        with cls.__table_count_lock:
            cls.__global_table_count = 0
            cls.__format_table_count = {}
