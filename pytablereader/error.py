# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import requests


class ValidationError(Exception):
    """
    Exception raised when data is not properly formatted.
    """


class InvalidNameError(Exception):
    """
    Base name error class.
    """


class InvalidTableNameError(InvalidNameError):
    """
    Exception raised when invalid table name used.
    """


class InvalidHeaderNameError(InvalidNameError):
    """
    Exception raised when table header name is invalid.
    """


class InvalidPathError(Exception):
    """
    Base path error class.
    """


class InvalidFilePathError(InvalidPathError):
    """
    Exception raised when invalid file path used.
    """


class InvalidUrlError(InvalidPathError):
    """
    Exception raised when invalid URL used.
    """


class InvalidDataError(ValueError):
    """
    Exception raised when data is invalid to load.
    """


class EmptyDataError(InvalidDataError):
    """
    Exception raised when data is not included valid table data.
    """


class OpenError(IOError):
    """
    Exception raised when failed to open a file.
    """


class LoaderNotFoundError(Exception):
    """
    Exception raised when appropriate loader not found.
    """


class HTTPError(requests.RequestException):
    """
    An HTTP error occurred.
    """
