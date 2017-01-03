# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import abc
import os.path

import dataproperty
import pathvalidate as pv
import six
from six.moves.urllib.parse import urlparse

from ._constant import SourceType
from .error import (
    EmptyDataError,
    InvalidFilePathError,
    InvalidUrlError
)


@six.add_metaclass(abc.ABCMeta)
class ValidatorInterface(object):

    @abc.abstractproperty
    def source_type(self):
        pass

    @abc.abstractmethod
    def validate(self):
        pass


class BaseValidator(ValidatorInterface):

    @property
    def source(self):
        return self.__source

    def __init__(self, source):
        self.__source = source


class FileValidator(BaseValidator):

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

    @property
    def source_type(self):
        return SourceType.TEXT

    def validate(self):
        if dataproperty.is_empty_string(self.source):
            raise EmptyDataError("data source is empty")


class UrlValidator(BaseValidator):

    @property
    def source_type(self):
        return SourceType.URL

    def validate(self):
        if dataproperty.is_empty_string(self.source):
            raise InvalidUrlError("url is empty")

        scheme = urlparse(self.source).scheme
        if scheme not in ["http", "https"]:
            raise InvalidUrlError(
                "invalid scheme: expected=http/https, actual={}".format(
                    scheme))
