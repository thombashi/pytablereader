# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import bs4
import dataproperty

from .._constant import TableNameTemplate as tnt
from ..data import TableData
from ..error import InvalidDataError
from ..formatter import TableFormatter


class HtmlTableFormatter(TableFormatter):

    @property
    def table_id(self):
        return self.__table_id

    def __init__(self, source_data):
        super(HtmlTableFormatter, self).__init__(source_data)

        if dataproperty.is_empty_string(source_data):
            raise InvalidDataError

        try:
            self.__soup = bs4.BeautifulSoup(self._source_data, "lxml")
        except bs4.FeatureNotFound:
            self.__soup = bs4.BeautifulSoup(self._source_data, "html.parser")

    def to_table_data(self):
        for table in self.__soup.find_all("table"):
            try:
                tabledata = self.__parse_html(table)
            except ValueError:
                continue

            if tabledata.is_empty_record():
                continue

            yield tabledata

    def _make_table_name(self):
        key = self.table_id
        if dataproperty.is_empty_string(key):
            key = self._loader.get_format_key()

        return self._loader._replace_table_name_template(
            self._loader._get_basic_tablename_mapping() +
            [(tnt.KEY, key)]
        )

    def __parse_html(self, table):
        header_list = []
        data_matrix = []

        self.__table_id = table.get("id")

        if self.__table_id is None:
            caption = table.find("caption")
            if caption is not None:
                caption = caption.text.strip()
                if dataproperty.is_not_empty_string(caption):
                    self.__table_id = caption

        row_list = table.find_all("tr")
        for row in row_list:
            col_list = row.find_all("td")
            if dataproperty.is_empty_sequence(col_list):
                th_list = row.find_all("th")
                if dataproperty.is_empty_sequence(th_list):
                    continue

                header_list = [row.text.strip() for row in th_list]
                continue

            data_list = [value.text.strip() for value in col_list]
            data_matrix.append(data_list)

        if dataproperty.is_empty_sequence(data_matrix):
            raise ValueError("data matrix is empty")

        self._loader.inc_table_count()

        return TableData(
            self._make_table_name(), header_list, data_matrix)
