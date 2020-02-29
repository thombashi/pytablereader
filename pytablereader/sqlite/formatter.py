"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import typepy
from tabledata import TableData

from pytablereader import DataError

from .._constant import TableNameTemplate as tnt
from ..formatter import TableFormatter


class SqliteTableFormatter(TableFormatter):
    def __init__(self, source_data):
        super().__init__(source_data)

        self.__table_name = None

        if typepy.is_null_string(source_data):
            raise DataError

    def to_table_data(self):
        from simplesqlite import SimpleSQLite
        from simplesqlite.query import AttrList

        con = SimpleSQLite(self._source_data, "r")

        for table in con.fetch_table_names():
            self.__table_name = table

            attr_names = con.fetch_attr_names(table)
            data_matrix = con.select(select=AttrList(attr_names), table_name=table).fetchall()

            yield TableData(
                table,
                attr_names,
                data_matrix,
                dp_extractor=self._loader.dp_extractor,
                type_hints=self._extract_type_hints(attr_names),
            )

    def _make_table_name(self):
        return self._loader._expand_table_name_format(
            self._loader._get_basic_tablename_keyvalue_mapping() + [(tnt.KEY, self.__table_name)]
        )
