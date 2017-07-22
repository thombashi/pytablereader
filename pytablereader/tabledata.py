# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
from decimal import Decimal
import hashlib
import re
import warnings

import six
import typepy

import dataproperty as dp
from six.moves import zip

from ._constant import PatternMatch
from ._logger import logger
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
    def value_matrix(self):
        """
        :return: Table data records.
        :rtype: list
        """

        return self.__record_list

    @property
    def record_list(self):
        # alias property of value_matrix. this method will be deleted in the
        # future

        return self.value_matrix

    def __init__(
            self, table_name, header_list, record_list, is_strip_quote=False):

        self.__dp_extractor = dp.DataPropertyExtractor()
        self.__dp_extractor.strip_str_header = '"'
        if is_strip_quote:
            self.__dp_extractor.strip_str_value = '"'

        self.__table_name = table_name
        self.__header_list = header_list
        self.__record_list = self.__to_record_list(record_list)

    def __repr__(self):
        element_list = [
            "table_name={}".format(self.table_name),
        ]

        try:
            element_list.append("header_list=[{}]".format(
                ", ".join(self.header_list)))
        except TypeError:
            element_list.append("header_list=None")

        element_list.append("rows={}".format(len(self.value_matrix)))

        return ", ".join(element_list)

    def __eq__(self, other):
        return all([
            self.table_name == other.table_name,
            self.header_list == other.header_list,
            all([
                all([
                    self.__compare_helper(lhs, rhs)
                    for lhs, rhs in zip(lhs_list, rhs_list)
                ])
                for lhs_list, rhs_list
                in zip(self.value_matrix, other.value_matrix)
            ]),
        ])

    def __ne__(self, other):
        return any([
            self.table_name != other.table_name,
            self.header_list != other.header_list,
            any([
                any([
                    not self.__compare_helper(lhs, rhs)
                    for lhs, rhs in zip(lhs_list, rhs_list)
                ])
                for lhs_list, rhs_list
                in zip(self.value_matrix, other.value_matrix)
            ]),
        ])

    def __hash__(self):
        body = (
            self.table_name +
            six.text_type(self.header_list) +
            six.text_type(self.value_matrix)
        )
        return hashlib.sha1(body.encode("utf-8")).hexdigest()

    def is_empty_header(self):
        """
        :return: |True| if the data :py:attr:`.header_list` is empty.
        :rtype: bool
        """

        return typepy.is_empty_sequence(self.header_list)

    def is_empty_record(self):
        """
        :return: |True| if the data :py:attr:`.value_matrix` is empty.
        :rtype: bool
        """

        return typepy.is_empty_sequence(self.value_matrix)

    def is_empty(self):
        """
        :return:
            |True| if the data :py:attr:`.header_list` or
            :py:attr:`.value_matrix` is empty.
        :rtype: bool
        """

        return any([self.is_empty_header(), self.is_empty_record()])

    def as_dict(self):
        """
        :return: Table data as a |dict| instance.
        :rtype: dict

        :Sample Code:
            .. code:: python

                from pytablereader import TableData

                TableData(
                    table_name="sample",
                    header_list=["a", "b"],
                    record_list=[[1, 2], [3.3, 4.4]]
                ).as_dict()
        :Output:
            .. code:: json

                {'sample': [{'a': 1, 'b': 2}, {'a': 3.3, 'b': 4.4}]}
        """

        self.__dp_extractor.float_type = float

        dict_body = []
        for value_list in self.value_matrix:
            if typepy.is_empty_sequence(value_list):
                continue

            dict_record = [
                (header, self.__dp_extractor.to_dataproperty(value).data)
                for header, value in zip(self.header_list, value_list)
                if value is not None
            ]

            if typepy.is_empty_sequence(dict_record):
                continue

            dict_body.append(OrderedDict(dict_record))

        return {self.table_name: dict_body}

    def asdict(self):
        warnings.warn(
            "asdict() will be deleted in the future, use as_dict instead.",
            DeprecationWarning)

        return self.as_dict()

    def as_dataframe(self):
        """
        :return: Table data as a ``pandas.DataFrame`` instance.
        :rtype: pandas.DataFrame

        :Example:
            :ref:`example-as-dataframe`

        .. note::
            ``pandas`` package required to execute this method.
        """

        import pandas

        dataframe = pandas.DataFrame(self.value_matrix)
        if not self.is_empty_header():
            dataframe.columns = self.header_list

        return dataframe

    def filter_column(
            self, pattern_list=None, is_invert_match=False,
            is_re_match=False, pattern_match=PatternMatch.OR):
        logger.debug(
            "filter_column: pattern_list={}, is_invert_match={}, "
            "is_re_match={}, pattern_match={}".format(
                pattern_list, is_invert_match, is_re_match, pattern_match))

        if not pattern_list:
            return TableData(
                table_name=self.table_name, header_list=self.header_list,
                record_list=self.value_matrix)

        match_header_list = []
        match_column_matrix = []

        if pattern_match == PatternMatch.OR:
            match_method = any
        elif pattern_match == PatternMatch.AND:
            match_method = all
        else:
            raise ValueError("unknown matching: {}".format(pattern_match))

        for header, column_value_list in zip(
                self.header_list, zip(*self.value_matrix)):
            is_match_list = []
            for pattern in pattern_list:
                is_match = self.__is_match(header, pattern, is_re_match)

                is_match_list.append(any([
                    is_match and not is_invert_match,
                    not is_match and is_invert_match,
                ]))

            if match_method(is_match_list):
                match_header_list.append(header)
                match_column_matrix.append(column_value_list)

        logger.debug(
            "filter_column: table={}, match_header_list={}".format(
                self.table_name, match_header_list))

        return TableData(
            table_name=self.table_name, header_list=match_header_list,
            record_list=zip(*match_column_matrix))

    @staticmethod
    def from_dataframe(dataframe, table_name=""):
        """
        Initialize TableData instance from a pandas.DataFrame instance.

        :param pandas.DataFrame dataframe:
        :param str table_name: Table name to create.
        """

        return TableData(
            table_name=table_name,
            header_list=list(dataframe.columns.values),
            record_list=dataframe.values.tolist())

    def __compare_helper(self, lhs, rhs):
        from typepy.type import Nan

        if Nan(lhs).is_type() and Nan(rhs).is_type():
            return True

        return lhs == rhs

    def __is_match(self, header, pattern, is_re_match):
        if is_re_match:
            return re.search(pattern, header) is not None

        return header == pattern

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
                self.__dp_extractor.to_dataproperty(values.get(header)).data
                for header in self.header_list
            ]
        except AttributeError:
            pass

        try:
            # namedtuple to list
            dict_value = values._asdict()
            return [
                self.__dp_extractor.to_dataproperty(
                    dict_value.get(header)).data
                for header in self.header_list
            ]
        except AttributeError:
            pass

        try:
            return [
                self.__dp_extractor.to_dataproperty(value).data
                for value in values
            ]
        except TypeError:
            raise InvalidDataError(
                "record must be a list or tuple: actual={}".format(values))

    def __to_record_list(self, record_list):
        """
        Convert matrix to records
        """

        self.__dp_extractor.float_type = Decimal

        if typepy.is_empty_sequence(self.header_list):
            return record_list

        return [
            self.__to_record(record)
            for record in record_list
        ]
