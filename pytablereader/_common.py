"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os.path
import posixpath
from urllib.parse import urlparse

import pathvalidate
import typepy

from ._constant import Default
from .error import InvalidFilePathError


try:
    import simplejson as json
except ImportError:
    import json  # type: ignore # noqa


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
        raise InvalidFilePathError(f"invalid URL path: {url_path}")

    temp_name = os.path.basename(url_path.rstrip("/"))
    if typepy.is_null_string(temp_name):
        temp_name = pathvalidate.replace_symbol(temp_name, replacement_text="_")

    if typepy.is_null_string(temp_name):
        raise InvalidFilePathError(f"invalid URL: {url}")

    try:
        return posixpath.join(temp_dir_path, temp_name)
    except (TypeError, AttributeError):
        raise InvalidFilePathError("temp_dir_path must be a string")
