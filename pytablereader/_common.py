# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import os.path

import dataproperty

from .error import InvalidFilePathError


def get_extension(file_path):
    if dataproperty.is_empty_string(file_path):
        raise InvalidFilePathError("file path is empty")

    return os.path.splitext(file_path)[1].lstrip(".")
