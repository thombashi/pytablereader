# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import typepy

from .._constant import TableNameTemplate as tnt
from ..error import InvalidDataError
from ..formatter import TableFormatter
from ..tabledata import TableData


class SqliteTableFormatter(TableFormatter):

    def __init__(self, source_data):
        super(SqliteTableFormatter, self).__init__(source_data)

        self.__table_name = None

        if typepy.is_null_string(source_data):
            raise InvalidDataError

    def to_table_data(self):
        from simplesqlite import SimpleSQLite
        from simplesqlite.sqlquery import SqlQuery

        con = SimpleSQLite(self._source_data, "r")

        for table in con.get_table_name_list():
            self.__table_name = table

            attr_name_list = con.get_attr_name_list(table)
            data_matrix = con.select(
                select=",".join(SqlQuery.to_attr_str_list(attr_name_list)),
                table_name=table)

            yield TableData(
                table, attr_name_list, data_matrix)

    def _make_table_name(self):
        return self._loader._expand_table_name_format(
            self._loader._get_basic_tablename_keyvalue_mapping() + [
                (tnt.KEY, self.__table_name),
            ])
