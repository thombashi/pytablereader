# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import hashlib

import dataproperty
import pytablewriter
import six


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

    def __init__(self, table_name, header_list, record_list):
        self.__table_name = table_name
        self.__header_list = header_list
        self.__record_list = record_list

    def __repr__(self):
        return "table_name={}, header_list={}, record_list={}".format(
            self.table_name, self.header_list, self.record_list)

    def __eq__(self, other):
        return all([
            self.table_name == other.table_name,
            self.header_list == other.header_list,
            self.record_list == other.record_list,
        ])

    def __hash__(self):
        body = self.table_name + str(self.header_list) + str(self.record_list)
        return hashlib.sha1(body.encode("utf-8")).hexdigest()

    def is_empty_header(self):
        """
        :return: |True| if the data :py:attr:`.header_list` is empty.
        :rtype: bool
        """

        return dataproperty.is_empty_sequence(self.header_list)

    def is_empty_record(self):
        """
        :return: |True| if the data :py:attr:`.record_list` is empty.
        :rtype: bool
        """

        return dataproperty.is_empty_sequence(self.record_list)

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

    def dumps(self):
        """
        :return: Formatted text for pretty print.
        :rtype: str

        :Examples:
            .. code:: python

                >>>print(tabledata.dumps())
                .. table:: sample_data

                    ======  ======  ======
                    attr_a  attr_b  attr_c
                    ======  ======  ======
                         1     4.0  a
                         2     2.1  bb
                         3   120.9  ccc
                    ======  ======  ======
        """

        writer = pytablewriter.RstSimpleTableWriter()
        writer.set_table_data(self)
        writer.stream = six.StringIO()
        writer.write_table()

        return writer.stream.getvalue()
