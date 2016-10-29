# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import hashlib

from .error import InvalidTableNameError
from .error import InvalidHeaderNameError
import dataproperty
import pathvalidate


def validate_table_name(name):
    """
    :param str name: Table name to validate.
    :raises InvalidTableNameError: |raises_validate_table_name|
    """

    try:
        pathvalidate.validate_sqlite_table_name(name)
    except pathvalidate.InvalidReservedNameError as e:
        raise InvalidTableNameError(e)
    except pathvalidate.NullNameError:
        raise InvalidTableNameError("table name is empty")
    except pathvalidate.InvalidCharError as e:
        raise InvalidTableNameError(e)


class TableData(object):
    """
    Class to represent a table data structure.
    """

    @property
    def table_name(self):
        """
        :return: The table name.
        :rtype: str
        """

        return self.__table_name

    @property
    def header_list(self):
        """
        :return: List of table header names.
        :rtype: list
        """

        return self.__header_list

    @property
    def record_list(self):
        """
        :return: List of table data records.
        :rtype: list
        """

        return self.__record_list

    def __init__(self, table_name, header_list, record_list):
        validate_table_name(table_name)

        self.__table_name = table_name
        self.__header_list = header_list
        self.__record_list = record_list

        self.__sanitize_header_list()

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

    def validate_header(self, header):
        """
        No operation.

        This method called for each table header.
        Override this method in subclass if you want to detect
        invalid table header element.
        Raise
        :py:class:`~pytablereader.error.InvalidHeaderNameError`
        if an element is invalid.

        :param string header: Table header name.
        """

    def rename_header(self, i):
        """
        This method called when :py:meth:`.validate_header` method raise
        :py:class:`~pytablereader.error.InvalidHeaderNameError`.
        Override this method in subclass if you want to rename invalid
        table header element.

        :param int i: Table header index.
        :return: Renamed header name.
        :rtype: str
        :raises pytablereader.error.InvalidHeaderNameError: Always raised.
        """

        raise InvalidHeaderNameError(self.header_list[i])

    def is_empty_record(self):
        """
        :return: ``True`` if the data records of the table is empty.
        :rtype: bool
        """

        return dataproperty.is_empty_sequence(self.record_list)

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

    def dumps(self, indent=4):
        """
        :return: Formatted text for pretty print.
        :rtype: str

        :Examples:
            .. code:: python

                >>>print(tabledata.dumps())
                TableData:
                    table_name: sample_data
                    header_list: attr_a, attr_b, attr_c
                    record_list:
                        ['1', '4', u'a']
                        ['2', '2.1', u'bb']
                        ['3', '120.9', u'ccc']
        """

        indent_str = " " * indent

        message_list = ["TableData:"]

        indent_level = 1
        message_list.extend([
            "{:s}table_name: {}".format(
                indent_str * indent_level, self.table_name),
            "{:s}header_list: {}".format(
                indent_str * indent_level, ", ".join(self.header_list)),
            "{:s}record_list:".format(indent_str * indent_level),
        ])

        indent_level += 1
        message_list.extend([
            "{:s}{}".format(indent_str * indent_level, record)
            for record in self.record_list
        ])

        return "\n".join(message_list)

    def __sanitize_header_list(self):
        new_header_list = []

        for i, header in enumerate(self.header_list):
            try:
                self.validate_header(header)
                new_header = header
            except InvalidHeaderNameError:
                new_header = self.rename_header(i)

            new_header_list.append(new_header)

        self.__header_list = new_header_list
