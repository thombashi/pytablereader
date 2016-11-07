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


class Test_make_temp_file_path_from_url:

    @pytest.mark.parametrize(["temp_dir_path", "value", "expected"], [
        [
            "/tmp",
            "https://raw.githubusercontent.com/valid/test/data/validext.csv",
            "/tmp/validext.csv"
        ],
        [
            "/tmp",
            "https://raw.githubusercontent.com/valid/test/data/validext/",
            "/tmp/validext"
        ],
    ])
    def test_normal(self, temp_dir_path, value, expected):
        assert make_temp_file_path_from_url(temp_dir_path, value) == expected

    @pytest.mark.parametrize(["temp_dir_path", "value", "expected"], [
        [None, "tmp", InvalidFilePathError],
        ["tmp", "", InvalidFilePathError],
        ["tmp", None, InvalidFilePathError],
    ])
    def test_null_table_name(self, temp_dir_path, value, expected):
        with pytest.raises(expected):
            make_temp_file_path_from_url(temp_dir_path, value)
