"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pathvalidate as pv
import typepy

from pytablereader import DataError, InvalidHeaderNameError

from .._common import get_file_encoding
from .._constant import TableNameTemplate as tnt
from .._logger import FileSourceLogger, TextSourceLogger
from .._validator import FileValidator, TextValidator
from ..interface import AbstractTableReader
from ..json.formatter import SingleJsonTableConverterA


class LtsvTableLoader(AbstractTableReader):
    """
    Abstract class of
    `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
    format table loaders.

    .. py:attribute:: encoding

        Encoding of the LTSV data.
    """

    @property
    def format_name(self):
        return "ltsv"

    def __init__(self, source, quoting_flags, type_hints, type_hint_rules=None):
        super().__init__(source, quoting_flags, type_hints, type_hint_rules)

        self._ltsv_input_stream = None

    def _to_data_matrix(self):
        from collections import OrderedDict

        data_matrix = []

        for row_idx, row in enumerate(self._ltsv_input_stream):
            if typepy.is_empty_sequence(row):
                continue

            ltsv_record = OrderedDict()
            for col_idx, ltsv_item in enumerate(row.strip().split("\t")):
                try:
                    label, value = ltsv_item.split(":")
                except ValueError:
                    raise DataError(
                        "invalid ltsv item found: line={}, col={}, item='{}'".format(
                            row_idx, col_idx, ltsv_item
                        )
                    )

                label = label.strip('"')

                try:
                    pv.validate_ltsv_label(label)
                except pv.ValidationError:
                    raise InvalidHeaderNameError(
                        "invalid label found (acceptable chars are [0-9A-Za-z_.-]): "
                        "line={}, col={}, label='{}'".format(row_idx, col_idx, label)
                    )

                ltsv_record[label] = value

            data_matrix.append(ltsv_record)

        # using generator to prepare for future enhancement to support
        # iterative load.
        yield data_matrix


class LtsvTableFileLoader(LtsvTableLoader):
    """
    `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
    format file loader class.

    :param str file_path: Path to the loading LTSV file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s``.
    """

    def __init__(self, file_path, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(file_path, quoting_flags, type_hints, type_hint_rules)

        self.encoding = None

        self._validator = FileValidator(file_path)
        self._logger = FileSourceLogger(self)

        self.__file = None

    def load(self):
        """
        Extract tabular data as |TableData| instances from a LTSV file.
        |load_source_desc_file|

        :return:
            Loaded table data.
            |load_table_name_desc|

            ===================  ========================================
            Format specifier     Value after the replacement
            ===================  ========================================
            ``%(filename)s``     |filename_desc|
            ``%(format_name)s``  ``"ltsv"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ========================================
        :rtype: |TableData| iterator
        :raises pytablereader.InvalidHeaderNameError:
            If an invalid label name is included in the LTSV file.
        :raises pytablereader.DataError:
            If the LTSV data is invalid.
        """

        self._validate()
        self._logger.logging_load()
        self.encoding = get_file_encoding(self.source, self.encoding)

        self._ltsv_input_stream = open(self.source, encoding=self.encoding)

        for data_matrix in self._to_data_matrix():
            formatter = SingleJsonTableConverterA(data_matrix)
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

    def __init__(self, text=None, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(text, quoting_flags, type_hints)

        self._validator = TextValidator(text)
        self._logger = TextSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a LTSV text object.
        |load_source_desc_text|

        :return:
            Loaded table data.
            |load_table_name_desc|

            ===================  ========================================
            Format specifier     Value after the replacement
            ===================  ========================================
            ``%(filename)s``     ``""``
            ``%(format_name)s``  ``"ltsv"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ========================================
        :rtype: |TableData| iterator
        :raises pytablereader.InvalidHeaderNameError:
            If an invalid label name is included in the LTSV file.
        :raises pytablereader.DataError:
            If the LTSV data is invalid.
        """

        self._validate()
        self._logger.logging_load()

        self._ltsv_input_stream = self.source.splitlines()

        for data_matrix in self._to_data_matrix():
            formatter = SingleJsonTableConverterA(data_matrix)
            formatter.accept(self)

            return formatter.to_table_data()

    def _get_default_table_name_template(self):
        return f"{tnt.FORMAT_NAME:s}{tnt.FORMAT_ID:s}"
