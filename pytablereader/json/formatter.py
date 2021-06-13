"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc

import jsonschema
from tabledata import TableData

from .._constant import SourceType
from .._constant import TableNameTemplate as tnt
from ..error import ValidationError
from ..formatter import TableFormatter


class JsonConverter(TableFormatter):
    """
    The abstract class of JSON data converter.
    """

    _VALUE_TYPE_SCHEMA = {
        "anyOf": [
            {"type": "string"},
            {"type": "number"},
            {"type": "boolean"},
            {"type": "null"},
            {"type": "object"},
        ]
    }

    def __init__(self, json_buffer):
        self._buffer = json_buffer

    @abc.abstractproperty
    def _schema(self):  # pragma: no cover
        pass

    def _validate_source_data(self):
        """
        :raises ValidationError:
        """

        try:
            jsonschema.validate(self._buffer, self._schema)
        except jsonschema.ValidationError as e:
            raise ValidationError(e)


class SingleJsonTableConverterBase(JsonConverter):
    def _make_table_name(self):
        kv_mapping = self._loader._get_basic_tablename_keyvalue_mapping()
        kv_mapping[tnt.KEY] = self._loader.get_format_key()

        if self._loader.source_type == SourceType.FILE:
            kv_mapping[tnt.DEFAULT] = tnt.FILENAME
        elif self._loader.source_type == SourceType.TEXT:
            kv_mapping[tnt.DEFAULT] = tnt.KEY

        return self._loader._expand_table_name_format(kv_mapping)


class SingleJsonTableConverterA(SingleJsonTableConverterBase):
    """
    A concrete class of JSON table data formatter.
    """

    @property
    def _schema(self):
        return {
            "type": "array",
            "items": {"type": "object", "additionalProperties": self._VALUE_TYPE_SCHEMA},
        }

    def to_table_data(self):
        """
        :raises ValueError:
        :raises pytablereader.error.ValidationError:
        """

        self._validate_source_data()

        attr_name_set = set()
        for json_record in self._buffer:
            attr_name_set = attr_name_set.union(json_record.keys())
        headers = sorted(attr_name_set)

        self._loader.inc_table_count()

        yield TableData(
            self._make_table_name(),
            headers,
            self._buffer,
            dp_extractor=self._loader.dp_extractor,
            type_hints=self._extract_type_hints(headers),
        )


class SingleJsonTableConverterB(SingleJsonTableConverterBase):
    """
    A concrete class of JSON table data formatter.
    """

    @property
    def _schema(self):
        return {
            "type": "object",
            "additionalProperties": {"type": "array", "items": self._VALUE_TYPE_SCHEMA},
        }

    def to_table_data(self):
        """
        :raises ValueError:
        :raises pytablereader.error.ValidationError:
        """

        self._validate_source_data()
        self._loader.inc_table_count()

        headers = sorted(self._buffer.keys())

        yield TableData(
            self._make_table_name(),
            headers,
            zip(*(self._buffer.get(header) for header in headers)),
            dp_extractor=self._loader.dp_extractor,
            type_hints=self._extract_type_hints(),
        )


class SingleJsonTableConverterC(SingleJsonTableConverterBase):
    """
    A concrete class of JSON table data formatter.
    """

    @property
    def _schema(self):
        return {"type": "object", "additionalProperties": self._VALUE_TYPE_SCHEMA}

    def to_table_data(self):
        """
        :raises ValueError:
        :raises pytablereader.error.ValidationError:
        """

        self._validate_source_data()
        self._loader.inc_table_count()

        yield TableData(
            self._make_table_name(),
            ["key", "value"],
            [record for record in self._buffer.items()],
            dp_extractor=self._loader.dp_extractor,
            type_hints=self._extract_type_hints(),
        )


class MultipleJsonTableConverterBase(JsonConverter):
    def __init__(self, json_buffer):
        super().__init__(json_buffer)

        self._table_key = None

    def _make_table_name(self):
        kv_mapping = self._loader._get_basic_tablename_keyvalue_mapping()
        kv_mapping[tnt.DEFAULT] = tnt.KEY
        kv_mapping[tnt.KEY] = self._table_key

        return self._loader._expand_table_name_format(kv_mapping)


class MultipleJsonTableConverterA(MultipleJsonTableConverterBase):
    """
    A concrete class of JSON table data converter.
    """

    @property
    def _schema(self):
        return {
            "type": "object",
            "additionalProperties": {
                "type": "array",
                "items": {"type": "object", "additionalProperties": self._VALUE_TYPE_SCHEMA},
            },
        }

    def to_table_data(self):
        """
        :raises ValueError:
        :raises pytablereader.error.ValidationError:
        """

        self._validate_source_data()

        for table_key, json_records in self._buffer.items():
            attr_name_set = set()
            for json_record in json_records:
                attr_name_set = attr_name_set.union(json_record.keys())
            headers = sorted(attr_name_set)

            self._loader.inc_table_count()
            self._table_key = table_key

            yield TableData(
                self._make_table_name(),
                headers,
                json_records,
                dp_extractor=self._loader.dp_extractor,
                type_hints=self._extract_type_hints(headers),
            )


class MultipleJsonTableConverterB(MultipleJsonTableConverterBase):
    """
    A concrete class of JSON table data converter.
    """

    @property
    def _schema(self):
        return {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"type": "array", "items": self._VALUE_TYPE_SCHEMA},
            },
        }

    def to_table_data(self):
        """
        :raises ValueError:
        :raises pytablereader.error.ValidationError:
        """

        self._validate_source_data()

        for table_key, json_records in self._buffer.items():
            headers = sorted(json_records.keys())

            self._loader.inc_table_count()
            self._table_key = table_key

            yield TableData(
                self._make_table_name(),
                headers,
                zip(*(json_records.get(header) for header in headers)),
                dp_extractor=self._loader.dp_extractor,
                type_hints=self._extract_type_hints(headers),
            )


class MultipleJsonTableConverterC(MultipleJsonTableConverterBase):
    """
    A concrete class of JSON table data converter.
    """

    @property
    def _schema(self):
        return {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": self._VALUE_TYPE_SCHEMA,
            },
        }

    def to_table_data(self):
        """
        :raises ValueError:
        :raises pytablereader.error.ValidationError:
        """

        self._validate_source_data()

        for table_key, json_records in self._buffer.items():
            self._loader.inc_table_count()
            self._table_key = table_key

            yield TableData(
                self._make_table_name(),
                ["key", "value"],
                [record for record in json_records.items()],
                dp_extractor=self._loader.dp_extractor,
                type_hints=self._extract_type_hints(),
            )


class JsonTableFormatter(TableFormatter):
    def to_table_data(self):
        converter_class_list = [
            MultipleJsonTableConverterA,
            MultipleJsonTableConverterB,
            MultipleJsonTableConverterC,
            SingleJsonTableConverterA,
            SingleJsonTableConverterB,
            SingleJsonTableConverterC,
        ]

        for converter_class in converter_class_list:
            converter = converter_class(self._source_data)
            converter.accept(self._loader)
            try:
                yield from converter.to_table_data()
                return
            except ValidationError:
                pass
            else:
                break

            """
            if not isinstance(self._source_data, (list, type)):
                continue

            for source in self._source_data:
                #print("!!", type(source), type(converter))
                converter = converter_class(source)
                converter.accept(self._loader)
                try:
                    yield from converter.to_table_data()
                    return
                except ValidationError:
                    pass
                else:
                    break
            """

        raise ValidationError(f"inconvertible JSON schema: json={self._source_data}")
