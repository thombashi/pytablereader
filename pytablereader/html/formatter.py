# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import re

import bs4
import dataproperty as dp

from .._constant import TableNameTemplate as tnt
from ..error import InvalidDataError
from ..formatter import TableFormatter
from ..tabledata import TableData


class HtmlTableFormatter(TableFormatter):

    @property
    def table_id(self):
        return self.__table_id

    def __init__(self, source_data):
        super(HtmlTableFormatter, self).__init__(source_data)

        self.__table_id = None

        if dp.is_empty_string(source_data):
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
        if dp.is_empty_string(key):
            key = self._loader.get_format_key()

        try:
            title = self.__soup.title.text
        except AttributeError:
            title = ""

        return self._loader._replace_table_name_template(
            self._loader._get_basic_tablename_mapping() + [
                (tnt.KEY, key),
                (tnt.TITLE, title),
            ]
        )

    def __parse_tag_id(self, table):
        self.__table_id = table.get("id")

        if self.__table_id is None:
            caption = table.find("caption")
            if caption is not None:
                caption = caption.text.strip()
                if dp.is_not_empty_string(caption):
                    self.__table_id = caption

    def __parse_html(self, table):
        header_list = []
        data_matrix = []

        self.__parse_tag_id(table)

        row_list = table.find_all("tr")
        re_table_val = re.compile("td|th")
        for row in row_list:
            td_list = row.find_all("td")
            if dp.is_empty_sequence(td_list):
                if dp.is_not_empty_sequence(header_list):
                    continue

                th_list = row.find_all("th")
                if dp.is_empty_sequence(th_list):
                    continue

                header_list = [row.text.strip() for row in th_list]
                continue

            data_matrix.append([
                value.get_text().strip()
                for value in row.find_all(re_table_val)
            ])

        if dp.is_empty_sequence(data_matrix):
            raise ValueError("data matrix is empty")

        self._loader.inc_table_count()

        return TableData(
            self._make_table_name(), header_list, data_matrix)
