# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import abc
import os.path

import pathvalidate as pv
import six
import typepy
from pytablereader import DataError
from six.moves.urllib.parse import urlparse

from ._constant import SourceType
from .error import InvalidFilePathError, UrlError


@six.add_metaclass(abc.ABCMeta)
class ValidatorInterface(object):
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
            pv.validate_file_path(self.source)
        except pv.NullNameError:
            raise InvalidFilePathError("file path is empty")
        except (ValueError, pv.InvalidCharError, pv.InvalidLengthError) as e:
            raise InvalidFilePathError(e)

        if not os.path.isfile(self.source):
            raise IOError("file not found")


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
            raise UrlError("invalid scheme: expected=http/https, actual={}".format(scheme))
