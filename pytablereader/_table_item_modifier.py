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
        self.__none_value = none_value
        self.__strip_str = strip_str
        self.__is_strict_int = is_strict_int
        self.__is_strict_float = is_strict_float

    def modify_header(self, header):
        return self.__strip_quote(header)

    def modify_data(self, input_data):
        try:
            data = self.__strip_quote(input_data)
        except AttributeError:
            if input_data is None:
                return self.__none_value

            data = input_data

        inttype = dp.IntegerType(data, is_strict=self.__is_strict_int)
        if inttype.is_convertible_type():
            return inttype.convert()

        floattype = dp.FloatType(data, is_strict=self.__is_strict_float)
        if floattype.is_convertible_type():
            return floattype.convert()

        return MultiByteStrDecoder(data).unicode_str

    def __strip_quote(self, value):
        return value.strip(self.__strip_str)
