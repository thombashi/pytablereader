# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import os.path
import posixpath

import pathvalidate
import typepy
from six.moves.urllib.parse import urlparse

from ._constant import Default
from .error import InvalidFilePathError


def get_file_encoding(file_path, encoding):
    from mbstrdecoder import detect_file_encoding

    if encoding:
        return encoding

    encoding = detect_file_encoding(file_path)
    if not encoding:
        return Default.ENCODING

    return encoding


def get_extension(file_path):
    if typepy.is_null_string(file_path):
        raise InvalidFilePathError("file path is empty")

    return os.path.splitext(file_path)[1].lstrip(".")


def make_temp_file_path_from_url(temp_dir_path, url):
    try:
        url_path = urlparse(url).path
    except AttributeError:
        raise InvalidFilePathError("url must be a string")

    if typepy.is_null_string(url_path):
        raise InvalidFilePathError("invalid URL path: {}".format(url_path))

    temp_name = os.path.basename(url_path.rstrip("/"))
    if typepy.is_null_string(temp_name):
        temp_name = pathvalidate.replace_symbol(temp_name, replacement_text="_")

    if typepy.is_null_string(temp_name):
        raise InvalidFilePathError("invalid URL: {}".format(url))

    try:
        return posixpath.join(temp_dir_path, temp_name)
    except (TypeError, AttributeError):
        raise InvalidFilePathError("temp_dir_path must be a string")
