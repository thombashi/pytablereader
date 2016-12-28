# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import dataproperty as dp
from mbstrdecoder import MultiByteStrDecoder


class TableItemModifier(object):

    def __init__(
            self, none_value=None, strip_str='"',
            is_strict_int=False, is_strict_float=False):
        self._none_value = none_value
        self._strip_str = strip_str
        self._is_strict_int = is_strict_int
        self._is_strict_float = is_strict_float

    def modify_header(self, header):
        return self._strip_quote(header)

    def modify_data(self, input_data):
        if input_data is None:
            return self._none_value

        data = self._preprocess_data(input_data)

        inttype = dp.IntegerType(data, is_strict=self._is_strict_int)
        if inttype.is_convertible_type():
            return inttype.convert()

        floattype = dp.FloatType(data, is_strict=self._is_strict_float)
        if floattype.is_convertible_type():
            return floattype.convert()

        return MultiByteStrDecoder(data).unicode_str

    def _preprocess_data(self, data):
        try:
            return self._strip_quote(data)
        except AttributeError:
            return data

    def _strip_quote(self, value):
        return value.strip(self._strip_str)


class JsonTableItemModifier(TableItemModifier):

    def modify_data(self, input_data):
        if input_data is None:
            return self._none_value

        data = self._preprocess_data(input_data)

        inttype = dp.IntegerType(data, is_strict=self._is_strict_int)
        if inttype.is_convertible_type():
            return inttype.convert()

        floattype = dp.FloatType(data, is_strict=self._is_strict_float)
        if floattype.is_convertible_type():
            return float(data)

        return MultiByteStrDecoder(data).unicode_str
