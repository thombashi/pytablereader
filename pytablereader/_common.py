# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import os.path
import posixpath

import dataproperty
import pathvalidate
from six.moves.urllib.parse import urlparse

from .error import InvalidFilePathError


def get_extension(file_path):
    if dataproperty.is_empty_string(file_path):
        raise InvalidFilePathError("file path is empty")

    return os.path.splitext(file_path)[1].lstrip(".")


def make_temp_file_path_from_url(temp_dir_path, url):
    try:
        url_path = urlparse(url).path
    except AttributeError:
        raise InvalidFilePathError("url must be a string")

    if dataproperty.is_empty_string(url_path):
        raise InvalidFilePathError("invalid URL path: {}".format(url_path))

    temp_name = os.path.basename(url_path.rstrip("/"))
    if dataproperty.is_empty_string(temp_name):
        temp_name = pathvalidate.replace_symbol(
            temp_name, replacement_text="_")

    if dataproperty.is_empty_string(temp_name):
        raise InvalidFilePathError("invalid URL: {}".format(url))

    try:
        return posixpath.join(temp_dir_path, temp_name)
    except (TypeError, AttributeError):
        raise InvalidFilePathError("temp_dir_path must be a string")
