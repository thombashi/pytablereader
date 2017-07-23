# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

from pytablereader import InvalidFilePathError
from pytablereader._common import (
    get_extension,
    convert_idx_to_alphabet,
    make_temp_file_path_from_url,
)
import pytest


class Test_get_extension(object):

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


class Test_convert_idx_to_alphabet(object):

    @pytest.mark.parametrize(["value", "expected"], [
        [
            range(30),
            [
                "A", "B", "C", "D", "E",
                "F", "G", "H", "I", "J",
                "K", "L", "M", "N", "O",
                "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y",
                "Z", "AA", "AB", "AC", "AD",
            ]
        ],
        [
            range(0, 900, 30),
            [
                "A", "AE", "BI", "CM", "DQ",
                "EU", "FY", "HC", "IG", "JK",
                "KO", "LS", "MW", "OA", "PE",
                "QI", "RM", "SQ", "TU", "UY",
                "WC", "XG", "YK", "ZO", "AAS",
                "ABW", "ADA", "AEE", "AFI", "AGM",
            ]
        ],
    ])
    def test_normal(self, value, expected):
        assert [convert_idx_to_alphabet(v) for v in value] == expected


class Test_make_temp_file_path_from_url(object):

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
