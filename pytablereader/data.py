# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import hashlib

import dataproperty as dp

from ._table_item_modifier import TableItemModifier
from .error import InvalidDataError


class TableData(object):
    """
    Class to represent a table data structure.

    :param str table_name: Name of the table.
    :param list header_list: Table header names.
    :param list record_list: Table data records.
    """

    @property
    def table_name(self):
        """
        :return: Name of the table.
        :rtype: str
        """

        return self.__table_name

    @property
    def header_list(self):
        """
        :return: Table header names.
        :rtype: list
        """

        return self.__header_list

    @property
    def record_list(self):
        """
        :return: Table data records.
        :rtype: list
        """

        return self.__record_list

    def __init__(
            self, table_name, header_list, record_list, item_modifier=None):
        if item_modifier is None:
            self.__item_modifier = TableItemModifier()
        else:
            self.__item_modifier = item_modifier

        self.__table_name = table_name
        self.__header_list = header_list
        self.__record_list = self.__to_record_list(record_list)

    def __repr__(self):
        return "table_name={}, header_list={}, record_list={}".format(
            self.table_name, self.header_list, self.record_list)

    def __eq__(self, rhs):
        return all([
            self.table_name == rhs.table_name,
            self.header_list == rhs.header_list,
            all([
                all([
                    self.__compare_helper(lhs, rhs)
                    for lhs, rhs in zip(lhs_list, rhs_list)
                ])
                for lhs_list, rhs_list
                in zip(self.record_list, rhs.record_list)
            ]),
        ])

    def __hash__(self):
        body = self.table_name + str(self.header_list) + str(self.record_list)
        return hashlib.sha1(body.encode("utf-8")).hexdigest()

    def is_empty_header(self):
        """
        :return: |True| if the data :py:attr:`.header_list` is empty.
        :rtype: bool
        """

        return dp.is_empty_sequence(self.header_list)

    def is_empty_record(self):
        """
        :return: |True| if the data :py:attr:`.record_list` is empty.
        :rtype: bool
        """

        return dp.is_empty_sequence(self.record_list)

    def is_empty(self):
        """
        :return:
            |True| if the data :py:attr:`.header_list` or
            :py:attr:`.record_list` is empty.
        :rtype: bool
        """

        return any([self.is_empty_header(), self.is_empty_record()])

    def as_dict(self):
        """
        :return: Table data as a dictionary.
        :rtype: dict
        """

        return {
            "table_name": self.table_name,
            "header_list": self.header_list,
            "record_list": self.record_list,
        }

    def as_dataframe(self):
        """
        :return: Table data as a Pandas data frame.
        :rtype: pandas.DataFrame

        .. note::
            ``Pandas`` package required to execute this method.
        """

        import pandas

        dataframe = pandas.DataFrame(self.record_list)
        dataframe.columns = self.header_list

        return dataframe

    def __compare_helper(self, lhs, rhs):
        if dp.NanType(lhs).is_type() and dp.NanType(rhs).is_type():
            return True

        return lhs == rhs

    def __convert(self, value):
        if value is None:
            return self.__none_value

        return value

    def __to_record(self, values):
        """
        Convert values to a record.

        :param values: Value to be converted.
        :type values: |dict|/|namedtuple|/|list|/|tuple|
        :raises ValueError: If the ``value`` is invalid.
        """

        try:
            # dictionary to list
            return [
                self.__item_modifier.modify_data(values.get(header))
                for header in self.header_list
            ]
        except AttributeError:
            pass

        try:
            # namedtuple to list
            dict_value = values._asdict()
            return [
                self.__item_modifier.modify_data(dict_value.get(header))
                for header in self.header_list
            ]
        except AttributeError:
            pass

        try:
            return [
                self.__item_modifier.modify_data(value) for value in values
            ]
        except TypeError:
            raise InvalidDataError(
                "record must be a list or tuple: actual={}".format(values))

    def __to_record_list(self, record_list):
        """
        Convert matrix to records
        """

        if dp.is_empty_sequence(self.header_list):
            return record_list

        return [
            self.__to_record(record)
            for record in record_list
        ]
