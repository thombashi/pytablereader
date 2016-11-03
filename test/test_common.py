# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import pytest

from pytablereader._common import *
from pytablereader import *


class Test_get_extension:

    @pytest.mark.parametrize(["value", "expected"], [
        ["test.txt", "txt"],
        [".csv", ""],
        ["html", ""],
    ])
    def test_normal(self, value, expected):
        assert get_extension(value) == expected

    @pytest.mark.parametrize(["value", "expected"], [
        ["", InvalidFilePathError],
        [None, InvalidFilePathError],
    ])
    def test_null_table_name(self, value, expected):
        with pytest.raises(expected):
            get_extension(value)
