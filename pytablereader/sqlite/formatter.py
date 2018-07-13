# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import typepy
from pytablereader import DataError
from tabledata import TableData

from .._constant import TableNameTemplate as tnt
from ..formatter import TableFormatter


class SqliteTableFormatter(TableFormatter):
    def __init__(self, source_data):
        super(SqliteTableFormatter, self).__init__(source_data)

        self.__table_name = None

        if typepy.is_null_string(source_data):
            raise DataError

    def to_table_data(self):
        from simplesqlite import SimpleSQLite
        from simplesqlite.query import AttrList

        con = SimpleSQLite(self._source_data, "r")

        for table in con.fetch_table_name_list():
            self.__table_name = table

            attr_name_list = con.fetch_attr_name_list(table)
            data_matrix = con.select(select=AttrList(attr_name_list), table_name=table).fetchall()

            yield TableData(
                table, attr_name_list, data_matrix, dp_extractor=self._loader.dp_extractor
            )

    def _make_table_name(self):
        return self._loader._expand_table_name_format(
            self._loader._get_basic_tablename_keyvalue_mapping() + [(tnt.KEY, self.__table_name)]
        )
