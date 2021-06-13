"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc
import os
import stat
from errno import EBADF, ENAMETOOLONG, ENOENT, ENOTDIR
from urllib.parse import urlparse

import pathvalidate as pv
import typepy

from pytablereader import DataError

from ._constant import SourceType
from ._logger import logger
from .error import InvalidFilePathError, UrlError


def is_fifo(file_path: str) -> bool:
    try:
        return stat.S_ISFIFO(os.stat(file_path).st_mode)
    except OSError as e:
        logger.error(f"errno: {e.errno}")

        if e.errno not in (EBADF, ENAMETOOLONG, ENOENT, ENOTDIR):
            raise

        return False
    except ValueError:
        return False


class ValidatorInterface(metaclass=abc.ABCMeta):
    """
    An interface class for data source validator.
    """

    @abc.abstractproperty
    def source_type(self):
        pass

    @abc.abstractmethod
    def validate(self):
        pass


class BaseValidator(ValidatorInterface):
    """
    An abstract base class for data source validator.
    """

    @property
    def source(self):
        return self.__source

    def __init__(self, source):
        self.__source = source


class NullValidator(BaseValidator):
    @property
    def source_type(self):
        return "null"

    def validate(self):
        pass


class FileValidator(BaseValidator):
    """
    Validator class for file data source.
    """

    @property
    def source_type(self):
        return SourceType.FILE

    def validate(self):
        try:
            pv.validate_filepath(self.source, platform="auto")
        except pv.ValidationError as e:
            raise InvalidFilePathError(e)

        if os.path.isfile(self.source) or is_fifo(self.source):
            return

        raise OSError("file not found")


class TextValidator(BaseValidator):
    """
    Validator class for text object data source.
    """

    @property
    def source_type(self):
        return SourceType.TEXT

    def validate(self):
        if typepy.is_null_string(self.source):
            raise DataError("data source is empty")


class UrlValidator(BaseValidator):
    """
    Validator class for URL data source.
    """

    @property
    def source_type(self):
        return SourceType.URL

    def validate(self):
        if typepy.is_null_string(self.source):
            raise UrlError("url is empty")

        scheme = urlparse(self.source).scheme
        if scheme not in ["http", "https"]:
            raise UrlError(f"invalid scheme: expected=http/https, actual={scheme}")
