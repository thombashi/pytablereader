"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import typepy
from tabledata import TableData

from pytablereader import DataError

from ..formatter import TableFormatter


class CsvTableFormatter(TableFormatter):
    def to_table_data(self):
        if typepy.is_empty_sequence(self._loader.headers):
            headers = self._source_data[0]

            if any([typepy.is_null_string(header) for header in headers]):
                raise DataError(
                    "the first line includes empty string item."
                    "all of the items should contain header name."
                    "actual={}".format(headers)
                )

            data_matrix = self._source_data[1:]
        else:
            headers = self._loader.headers
            data_matrix = self._source_data

        if not data_matrix:
            raise DataError("data row must be greater or equal than one")

        self._loader.inc_table_count()

        yield TableData(
            self._loader.make_table_name(),
            headers,
            data_matrix,
            dp_extractor=self._loader.dp_extractor,
            type_hints=self._extract_type_hints(headers),
        )
