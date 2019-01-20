# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

from decimal import Decimal

import pytest
import typepy
from tabledata import TableData


try:
    import pandas

    PANDAS_IMPORT = True
except ImportError:
    PANDAS_IMPORT = False


@pytest.mark.skipif("PANDAS_IMPORT is False")
class Test_TableData_as_dataframe(object):
    @pytest.mark.parametrize(
        ["table_name", "headers", "rows"],
        [
            ["normal", ["a", "b"], [[10, 11], [20, 21]]],
            ["normal", None, [[10, 11], [20, 21]]],
            ["normal", None, None],
        ],
    )
    def test_normal(self, table_name, headers, rows):
        tabledata = TableData(table_name, headers, rows)
        dataframe = pandas.DataFrame(rows)
        if typepy.is_not_empty_sequence(headers):
            dataframe.columns = headers

        print("lhs: {}".format(tabledata.as_dataframe()))
        print("rhs: {}".format(dataframe))

        assert tabledata.as_dataframe().equals(dataframe)


@pytest.mark.skipif("PANDAS_IMPORT is False")
class Test_TableData_from_dataframe(object):
    def test_normal(self):
        dataframe = pandas.DataFrame(
            [[0, 0.1, "a"], [1, 1.1, "bb"], [2, 2.2, "ccc"]], columns=["id", "value", "name"]
        )
        expected = TableData(
            "tablename",
            ["id", "value", "name"],
            [[0, Decimal("0.1"), "a"], [1, Decimal("1.1"), "bb"], [2, Decimal("2.2"), "ccc"]],
        )

        assert TableData.from_dataframe(dataframe, "tablename").equals(expected)
