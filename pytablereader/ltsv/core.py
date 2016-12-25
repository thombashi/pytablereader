# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import io

import dataproperty as dp
import pathvalidate as pv
from six.moves import zip

from .._constant import TableNameTemplate as tnt
from .._validator import (
    FileValidator,
    TextValidator
)
from ..error import (
    InvalidHeaderNameError,
    InvalidDataError
)
from ..interface import TableLoader
from ..json.formatter import SingleJsonTableConverter


class LtsvTableLoader(TableLoader):
    """
    Abstract class of
    `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
    format table loader.

    .. py:attribute:: encoding

        Encoding of the LTSV data.
    """

    def __init__(self, source):
        super(LtsvTableLoader, self).__init__(source)

        self.encoding = "utf-8"

        self._ltsv_input_stream = None

    @property
    def format_name(self):
        return "ltsv"

    def _to_data_matrix(self):
        from collections import OrderedDict

        data_matrix = []

        for row_idx, row in enumerate(self._ltsv_input_stream):
            if dp.is_empty_sequence(row):
                continue

            ltsv_record = OrderedDict()
            for col_idx, ltsv_item in enumerate(row.strip().split("\t")):
                try:
                    label, value = ltsv_item.split(":")
                except ValueError:
                    raise InvalidDataError(
                        "invalid lstv item found: line={}, col={}, item='{}'".format(
                            row_idx, col_idx, ltsv_item))

                try:
                    label = label.strip('"')
                except AttributeError:
                    raise InvalidHeaderNameError(
                        "label must be a str: line={}, col={}, label='{}'".format(
                            row_idx, col_idx, label))

                try:
                    pv.validate_ltsv_label(label)
                except (pv.NullNameError, pv.InvalidCharError):
                    raise InvalidHeaderNameError(
                        "invalid label found (acceptable chars are [[0-9A-Za-z_.-]]): "
                        "line={}, col={}, label='{}'".format(
                            row_idx, col_idx, label))

                ltsv_record[label] = value

            data_matrix.append(ltsv_record)

        return data_matrix


class LtsvTableFileLoader(LtsvTableLoader):
    """
    `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
    format file loader class.

    :param str file_path: Path to the loading LTSV file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s``.
    """

    def __init__(self, file_path):
        super(LtsvTableFileLoader, self).__init__(file_path)

        self._validator = FileValidator(file_path)

        self.__file = None

    def load(self):
        """
        Extract tabular data as |TableData| incetances from a LTSV file.
        |load_source_desc_file|

        :return:
            Loaded table data.
            |load_table_name_desc|

            ===================  ========================================
            format specifier     value after the replacement
            ===================  ========================================
            ``%(filename)s``     |filename_desc|
            ``%(format_name)s``  ``"ltsv"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ========================================
        :rtype: |TableData| iterator
        :raises pytablereader.InvalidHeaderNameError:
            If an invalid label name is included in the LTSV file.
        :raises pytablereader.InvalidDataError:
            If the LTSV data is invalid.
        """

        self._validate()
        pv.validate_file_path(self.source)

        self._ltsv_input_stream = io.open(
            self.source, "r", encoding=self.encoding)

        formatter = SingleJsonTableConverter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return tnt.FILENAME


class LtsvTableTextLoader(LtsvTableLoader):
    """
    `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
    format text loader class.

    :param str text: LTSV text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(format_name)s%(format_id)s``.
    """

    def __init__(self, text):
        super(LtsvTableTextLoader, self).__init__(text)

        self._validator = TextValidator(text)

    def load(self):
        """
        Extract tabular data as |TableData| incetances from a LTSV text object.
        |load_source_desc_text|

        :return:
            Loaded table data.
            |load_table_name_desc|

            ===================  ========================================
            format specifier     value after the replacement
            ===================  ========================================
            ``%(filename)s``     ``""``
            ``%(format_name)s``  ``"ltsv"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ========================================
        :rtype: |TableData| iterator
        :raises pytablereader.InvalidHeaderNameError:
            If an invalid label name is included in the LTSV file.
        :raises pytablereader.InvalidDataError:
            If the LTSV data is invalid.
        """

        self._validate()

        self._ltsv_input_stream = self.source.splitlines()

        formatter = SingleJsonTableConverter(self._to_data_matrix())
        formatter.accept(self)

        return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return "{:s}{:s}".format(tnt.FORMAT_NAME, tnt.FORMAT_ID)
