"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

from pytablereader import set_logger
from pytablereader._logger._null_logger import NullLogger


class Test_set_logger:
    @pytest.mark.parametrize(["value"], [[True], [False]])
    def test_smoke(self, value):
        set_logger(value)


class Test_NullLogger:
    @pytest.mark.parametrize(["value"], [[True], [False]])
    def test_smoke(self, value, monkeypatch):
        monkeypatch.setattr("pytablereader._logger._logger.logger", NullLogger())
        set_logger(value)
