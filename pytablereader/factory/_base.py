"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc
import warnings

from mbstrdecoder import MultiByteStrDecoder

from .._constant import Default
from ..error import LoaderNotFoundError


class BaseTableLoaderFactory(metaclass=abc.ABCMeta):
    @property
    def source(self):
        """
        :return: Data source to load.
        :rtype: str
        """

        return self._source

    def __init__(self, source, encoding=None):
        if not encoding:
            self._encoding = Default.ENCODING
        else:
            self._encoding = encoding

        self._source = MultiByteStrDecoder(source, [encoding]).unicode_str

    @abc.abstractmethod
    def create_from_path(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def create_from_format_name(self, format_name):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _get_extension_loader_mapping(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _get_format_name_loader_mapping(self):  # pragma: no cover
        pass

    def get_format_names(self):
        """
        :return: Available format names.
        :rtype: list
        """

        return sorted(self._get_format_name_loader_mapping())

    def get_format_name_list(self):
        warnings.warn("'get_format_name_list' has moved to 'get_format_names'", DeprecationWarning)
        return self.get_format_names()

    def get_extensions(self):
        """
        :return: Available format file extensions.
        :rtype: list
        """

        return sorted(self._get_extension_loader_mapping())

    def get_extension_list(self):
        warnings.warn("'get_extension_list' has moved to 'get_extensions'", DeprecationWarning)
        return self.get_extensions()

    def _get_loader_class(self, loader_mapping, format_name):
        try:
            format_name = format_name.casefold()
        except AttributeError:
            raise TypeError("format name must be a string")

        try:
            return loader_mapping[format_name]
        except KeyError:
            raise LoaderNotFoundError(
                ", ".join(
                    [
                        f"loader not found: format='{format_name}'",
                        f"source='{self.source}'",
                    ]
                )
            )

    def _create_from_extension(self, extension):
        try:
            loader = self._get_loader_class(self._get_extension_loader_mapping(), extension)(
                self.source
            )

            return self._post_create(loader, extension=extension)
        except LoaderNotFoundError as e:
            raise LoaderNotFoundError(
                "\n".join(
                    [
                        f"{e.args[0]:s} (unknown extension).",
                        "",
                        "acceptable extensions are: {}.".format(", ".join(self.get_extensions())),
                        f"actual: '{extension}'",
                    ]
                )
            )

    def _create_from_format_name(self, format_name):
        try:
            loader = self._get_loader_class(self._get_format_name_loader_mapping(), format_name)(
                self.source
            )

            return self._post_create(loader, format_name=format_name)
        except LoaderNotFoundError as e:
            raise LoaderNotFoundError(
                "\n".join(
                    [
                        f"{e.args[0]:s} (unknown format name).",
                        "acceptable format names are: {}.".format(
                            ", ".join(self.get_format_names())
                        ),
                    ]
                )
            )

    def _post_create(self, loader, **kwargs):
        loader.encoding = self._encoding

        if loader.format_name == "csv" and kwargs.get("format_name") == "ssv":
            loader.delimiter = " "

        return loader
