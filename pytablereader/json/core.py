"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc
from collections import OrderedDict

from .._common import get_file_encoding, json
from .._constant import SourceType
from .._constant import TableNameTemplate as tnt
from .._logger import FileSourceLogger, TextSourceLogger
from .._validator import FileValidator, NullValidator, TextValidator
from ..error import ValidationError
from ..interface import AbstractTableReader
from .formatter import JsonTableFormatter


class JsonTableLoader(AbstractTableReader, metaclass=abc.ABCMeta):
    """
    An abstract class of JSON table loaders.
    """

    @property
    def format_name(self):
        return "json"

    @abc.abstractmethod
    def load_dict(self):  # pragma: no cover
        pass


class JsonTableFileLoader(JsonTableLoader):
    """
    A file loader class to extract tabular data from JSON files.

    :param str file_path: Path to the loading JSON file.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(filename)s_%(key)s``.
    """

    def __init__(self, file_path=None, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(file_path, quoting_flags, type_hints, type_hint_rules)

        self.encoding = None

        self._validator = FileValidator(file_path)
        self._logger = FileSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a JSON file.
        |load_source_desc_file|

        This method can be loading four types of JSON formats:

        **(1)** Single table data in a file:

            .. code-block:: json
                :caption: Acceptable JSON Schema (1): single table

                {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "number"},
                                {"type": "boolean"},
                                {"type": "null"}
                            ]
                        }
                    }
                }

            .. code-block:: json
                :caption: Acceptable JSON example for the JSON schema (1)

                [
                    {"attr_b": 4, "attr_c": "a", "attr_a": 1},
                    {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
                    {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
                ]

            The example data will be loaded as the following tabular data:

                .. table::

                    +------+------+------+
                    |attr_a|attr_b|attr_c|
                    +======+======+======+
                    |     1|   4.0|a     |
                    +------+------+------+
                    |     2|   2.1|bb    |
                    +------+------+------+
                    |     3| 120.9|ccc   |
                    +------+------+------+

        **(2)** Single table data in a file:

            .. code-block:: json
                :caption: Acceptable JSON Schema (2): single table

                {
                    "type": "object",
                    "additionalProperties": {
                        "type": "array",
                        "items": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "number"},
                                {"type": "boolean"},
                                {"type": "null"}
                            ]
                        }
                    }
                }

            .. code-block:: json
                :caption: Acceptable JSON example for the JSON schema (2)

                {
                    "attr_a": [1, 2, 3],
                    "attr_b": [4, 2.1, 120.9],
                    "attr_c": ["a", "bb", "ccc"]
                }

            The example data will be loaded as the following tabular data:

                .. table::

                    +------+------+------+
                    |attr_a|attr_b|attr_c|
                    +======+======+======+
                    |     1|   4.0|a     |
                    +------+------+------+
                    |     2|   2.1|bb    |
                    +------+------+------+
                    |     3| 120.9|ccc   |
                    +------+------+------+

        **(3)** Single table data in a file:

            .. code-block:: json

                :caption: Acceptable JSON Schema (3): single table

                {
                    "type": "object",
                    "additionalProperties": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "number"},
                            {"type": "boolean"},
                            {"type": "null"}
                        ]
                    }
                }

            .. code-block:: json
                :caption: Acceptable JSON example for the JSON schema (3)

                {
                    "num_ratings": 27,
                    "support_threads": 1,
                    "downloaded": 925716,
                    "last_updated":"2017-12-01 6:22am GMT",
                    "added":"2010-01-20",
                    "num": 1.1,
                    "hoge": null
                }

            The example data will be loaded as the following tabular data:

                .. table::

                    +---------------+---------------------+
                    |      key      |        value        |
                    +===============+=====================+
                    |num_ratings    |                   27|
                    +---------------+---------------------+
                    |support_threads|                    1|
                    +---------------+---------------------+
                    |downloaded     |               925716|
                    +---------------+---------------------+
                    |last_updated   |2017-12-01 6:22am GMT|
                    +---------------+---------------------+
                    |added          |2010-01-20           |
                    +---------------+---------------------+
                    |num            |                  1.1|
                    +---------------+---------------------+
                    |hoge           |None                 |
                    +---------------+---------------------+

        **(4)** Multiple table data in a file:

            .. code-block:: json
                :caption: Acceptable JSON Schema (4): multiple tables

                {
                    "type": "object",
                    "additionalProperties": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": {
                                "anyOf": [
                                    {"type": "string"},
                                    {"type": "number"},
                                    {"type": "boolean"},
                                    {"type": "null"}
                                ]
                            }
                        }
                    }
                }

            .. code-block:: json
                :caption: Acceptable JSON example for the JSON schema (4)

                {
                    "table_a" : [
                        {"attr_b": 4, "attr_c": "a", "attr_a": 1},
                        {"attr_b": 2.1, "attr_c": "bb", "attr_a": 2},
                        {"attr_b": 120.9, "attr_c": "ccc", "attr_a": 3}
                    ],
                    "table_b" : [
                        {"a": 1, "b": 4},
                        {"a": 2 },
                        {"a": 3, "b": 120.9}
                    ]
                }

            The example data will be loaded as the following tabular data:

                .. table:: table_a

                    +------+------+------+
                    |attr_a|attr_b|attr_c|
                    +======+======+======+
                    |     1|   4.0|a     |
                    +------+------+------+
                    |     2|   2.1|bb    |
                    +------+------+------+
                    |     3| 120.9|ccc   |
                    +------+------+------+

                .. table:: table_b

                    +-+-----+
                    |a|  b  |
                    +=+=====+
                    |1|  4.0|
                    +-+-----+
                    |2| None|
                    +-+-----+
                    |3|120.9|
                    +-+-----+

        **(5)** Multiple table data in a file:

            .. code-block:: json
                :caption: Acceptable JSON Schema (5): multiple tables

                {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "array",
                            "items": {
                                "anyOf": [
                                    {"type": "string"},
                                    {"type": "number"},
                                    {"type": "boolean"},
                                    {"type": "null"}
                                ]
                            }
                        }
                    }
                }

            .. code-block:: json
                :caption: Acceptable JSON example for the JSON schema (5)

                {
                    "table_a" : {
                        "attr_a": [1, 2, 3],
                        "attr_b": [4, 2.1, 120.9],
                        "attr_c": ["a", "bb", "ccc"]
                    },
                    "table_b" : {
                        "a": [1, 3],
                        "b": [4, 120.9]
                    }
                }

            The example data will be loaded as the following tabular data:

                .. table:: table_a

                    +------+------+------+
                    |attr_a|attr_b|attr_c|
                    +======+======+======+
                    |     1|   4.0|a     |
                    +------+------+------+
                    |     2|   2.1|bb    |
                    +------+------+------+
                    |     3| 120.9|ccc   |
                    +------+------+------+

                .. table:: table_b

                    +-+-----+
                    |a|  b  |
                    +=+=====+
                    |1|  4.0|
                    +-+-----+
                    |3|120.9|
                    +-+-----+

        **(6)** Multiple table data in a file:

            .. code-block:: json
                :caption: Acceptable JSON Schema (6): multiple tables

                {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "additionalProperties": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "number"},
                                {"type": "boolean"},
                                {"type": "null"}
                            ]
                        }
                    }
                }

            .. code-block:: json
                :caption: Acceptable JSON example for the JSON schema (6)

                {
                    "table_a": {
                        "num_ratings": 27,
                        "support_threads": 1,
                        "downloaded": 925716,
                        "last_updated":"2017-12-01 6:22am GMT",
                        "added":"2010-01-20",
                        "num": 1.1,
                        "hoge": null
                    },
                    "table_b": {
                        "a": 4,
                        "b": 120.9
                    }
                }

            The example data will be loaded as the following tabular data:

                .. table:: table_a

                    +---------------+---------------------+
                    |      key      |        value        |
                    +===============+=====================+
                    |num_ratings    |                   27|
                    +---------------+---------------------+
                    |support_threads|                    1|
                    +---------------+---------------------+
                    |downloaded     |               925716|
                    +---------------+---------------------+
                    |last_updated   |2017-12-01 6:22am GMT|
                    +---------------+---------------------+
                    |added          |2010-01-20           |
                    +---------------+---------------------+
                    |num            |                  1.1|
                    +---------------+---------------------+
                    |hoge           |None                 |
                    +---------------+---------------------+


                .. table:: table_b

                    +---+-----+
                    |key|value|
                    +===+=====+
                    |a  |  4.0|
                    +---+-----+
                    |b  |120.9|
                    +---+-----+

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            Format specifier     Value after the replacement
            ===================  ==============================================
            ``%(filename)s``     |filename_desc|
            ``%(key)s``          | This replaced the different value
                                 | for each single/multiple JSON tables:
                                 | [single JSON table]
                                 | ``%(format_name)s%(format_id)s``
                                 | [multiple JSON table] Table data key.
            ``%(format_name)s``  ``"json"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator
        :raises pytablereader.DataError:
            If the data is invalid JSON.
        :raises pytablereader.error.ValidationError:
            If the data is not acceptable JSON format.
        """

        formatter = JsonTableFormatter(self.load_dict())
        formatter.accept(self)

        return formatter.to_table_data()

    def load_dict(self):
        self._validate()
        self._logger.logging_load()
        self.encoding = get_file_encoding(self.source, self.encoding)

        with open(self.source, encoding=self.encoding) as fp:
            try:
                return json.load(fp, object_pairs_hook=OrderedDict)
            except ValueError as e:
                raise ValidationError(e)

    def _get_default_table_name_template(self):
        return f"{tnt.FILENAME:s}_{tnt.KEY:s}"


class JsonTableTextLoader(JsonTableLoader):
    """
    A text loader class to extract tabular data from JSON text data.

    :param str text: JSON text to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(key)s``.
    """

    @property
    def source_type(self):
        return SourceType.TEXT

    def __init__(self, text, quoting_flags=None, type_hints=None, type_hint_rules=None):
        super().__init__(text, quoting_flags, type_hints, type_hint_rules)

        self._validator = TextValidator(text)
        self._logger = TextSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a JSON text object.
        |load_source_desc_text|

        :return:
            Loaded table data iterator.
            |load_table_name_desc|

            ===================  ==============================================
            Format specifier     Value after the replacement
            ===================  ==============================================
            ``%(filename)s``     ``""``
            ``%(key)s``          | This replaced the different value
                                 | for each single/multiple JSON tables:
                                 | [single JSON table]
                                 | ``%(format_name)s%(format_id)s``
                                 | [multiple JSON table] Table data key.
            ``%(format_name)s``  ``"json"``
            ``%(format_id)s``    |format_id_desc|
            ``%(global_id)s``    |global_id|
            ===================  ==============================================
        :rtype: |TableData| iterator

        .. seealso::

            :py:meth:`.JsonTableFileLoader.load()`
        """

        formatter = JsonTableFormatter(self.load_dict())
        formatter.accept(self)

        return formatter.to_table_data()

    def load_dict(self):
        self._validate()
        self._logger.logging_load()

        return json.loads(self.source, object_pairs_hook=OrderedDict)

    def _get_default_table_name_template(self):
        return f"{tnt.KEY:s}"


class JsonTableDictLoader(JsonTableLoader):
    """
    A text loader class to extract tabular data from dict.

    :param str data: dict to load.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(key)s``.
    """

    @property
    def source_type(self):
        return SourceType.OBJECT

    def __init__(self, data, quoting_flags=None, type_hints=None):
        super().__init__(data, quoting_flags, type_hints)

        self._validator = NullValidator(data)
        self._logger = TextSourceLogger(self)

    def load(self):
        """
        Extract tabular data as |TableData| instances from a dict object.
        |load_source_desc_text|

        :rtype: |TableData| iterator

        .. seealso::

            :py:meth:`.JsonTableFileLoader.load()`
        """

        self._validate()
        self._logger.logging_load()

        formatter = JsonTableFormatter(self.source)
        formatter.accept(self)

        return formatter.to_table_data()

    def load_dict(self):
        return self.source

    def _get_default_table_name_template(self):
        return f"{tnt.KEY:s}"
