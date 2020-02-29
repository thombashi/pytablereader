"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import jsonschema
from tabledata import TableData

from ..error import ValidationError
from ..formatter import TableFormatter
from ..json.formatter import SingleJsonTableConverterBase


class FlatJsonTableConverter(SingleJsonTableConverterBase):
    """
    A concrete class of JSON table data formatter.
    """

    @property
    def _schema(self):
        return {"type": "object", "additionalProperties": self._VALUE_TYPE_SCHEMA}

    def _validate_source_data(self):
        for json_record in self._buffer:
            try:
                jsonschema.validate(json_record, self._schema)
            except jsonschema.ValidationError as e:
                raise ValidationError(e)

    def to_table_data(self):
        """
        :raises ValueError:
        :raises pytablereader.error.ValidationError:
        """

        self._validate_source_data()

        header_list = []
        for json_record in self._buffer:
            for key in json_record:
                if key not in header_list:
                    header_list.append(key)

        self._loader.inc_table_count()

        yield TableData(
            self._make_table_name(),
            header_list,
            self._buffer,
            dp_extractor=self._loader.dp_extractor,
            type_hints=self._extract_type_hints(header_list),
        )


class JsonLinesTableFormatter(TableFormatter):
    def to_table_data(self):
        converter = FlatJsonTableConverter(self._source_data)
        converter.accept(self._loader)

        return converter.to_table_data()
