# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from decimal import Decimal

import dataproperty as dp


class TableItemModifier(object):

    def __init__(self, none_value=None, strip_str='"', float_type=None):
        self._none_value = none_value
        self._strip_str = strip_str

        if float_type is None:
            self._float_type = Decimal
        else:
            self._float_type = float_type

    def modify_header(self, header):
        return self._strip_quote(header)

    def modify_data(self, input_data):
        return dp.DataProperty(
            self._preprocess_data(input_data),
            none_value=self._none_value,
            float_type=self._float_type).data

    def _preprocess_data(self, data):
        try:
            return self._strip_quote(data)
        except AttributeError:
            return data

    def _strip_quote(self, value):
        return value.strip(self._strip_str)
