"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import re
import sys

from typepy import Integer, RealNumber, String


TYPE_HINT_RULES = {
    re.compile("[ -_]text$", re.IGNORECASE): String,
    re.compile("[ -_]integer$", re.IGNORECASE): Integer,
    re.compile("[ -_]real$", re.IGNORECASE): RealNumber,
}


def fifo_writer(fifo_name, text):
    with open(fifo_name, "w") as p:
        p.write(text)


def print_test_result(expected, actual, error=None):
    print(f"[expected]\n{expected}\n")
    print(f"[actual]\n{actual}\n")

    if error:
        print(error, file=sys.stderr)
