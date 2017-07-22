# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

from decimal import Decimal

from pytablereader import TableData
import pytest
import typepy


try:
    import pandas
    PANDAS_IMPORT = True
except ImportError:
    PANDAS_IMPORT = False


@pytest.mark.skipif("PANDAS_IMPORT is False")
class Test_TableData_as_dataframe(object):

    @pytest.mark.parametrize(
        ["table_name", "header_list", "record_list"], [
            ["normal", ["a", "b"], [[10, 11], [20, 21]]],
            ["normal", None, [[10, 11], [20, 21]]],
            ["normal", None, None],
        ])
    def test_normal(self, table_name, header_list, record_list):
        tabledata = TableData(table_name, header_list, record_list)
        dataframe = pandas.DataFrame(record_list)
        if typepy.is_not_empty_sequence(header_list):
            dataframe.columns = header_list

        print("lhs: {}".format(tabledata.as_dataframe()))
        print("rhs: {}".format(dataframe))

        assert tabledata.as_dataframe().equals(dataframe)


@pytest.mark.skipif("PANDAS_IMPORT is False")
class Test_TableData_from_dataframe(object):

    def test_normal(self):
        dataframe = pandas.DataFrame(
            [
                [0, 0.1, "a"],
                [1, 1.1, "bb"],
                [2, 2.2, "ccc"],
            ],
            columns=['id', 'value', 'name'])
        expected = TableData(
            table_name="tablename",
            header_list=['id', 'value', 'name'],
            record_list=[
                [0, Decimal('0.1'), 'a'],
                [1, Decimal('1.1'), 'bb'],
                [2, Decimal('2.2'), 'ccc'],
            ])

        assert TableData.from_dataframe(dataframe, "tablename") == expected
