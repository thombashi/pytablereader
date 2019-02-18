# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, print_function, unicode_literals

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
    print("[expected]\n{}\n".format(expected))
    print("[actual]\n{}\n".format(actual))

    if error:
        print(error, file=sys.stderr)
