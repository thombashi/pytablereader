# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import abc

import dataproperty
import six

from ._null_logger import NullLogger


MODULE_NAME = "pytablereader"
_is_enable = False

try:
    from loguru import logger

    logger.disable(MODULE_NAME)
except ImportError:
    logger = NullLogger()


def set_logger(is_enable):
    global _is_enable

    if is_enable == _is_enable:
        return

    _is_enable = is_enable

    if is_enable:
        logger.enable(MODULE_NAME)
    else:
        logger.disable(MODULE_NAME)

    dataproperty.set_logger(is_enable)

    try:
        import simplesqlite

        simplesqlite.set_logger(is_enable)
    except ImportError:
        pass


def set_log_level(log_level):
    # deprecated
    return


def typehints_to_str(type_hints):
    return ", ".join([type_hint.__name__ if type_hint else "none" for type_hint in type_hints])


@six.add_metaclass(abc.ABCMeta)
class LoggerInterface(object):
    @abc.abstractmethod
    def logging_load(self):  # pragma: no cover
        pass


class BaseLogger(LoggerInterface):
    def __init__(self, loader):
        self._loader = loader

    def logging_load(self):
        logger.debug(self._get_load_message())

    def logging_table(self, table_data):
        logger.debug("loaded tabledata: {}".format(table_data))

    @abc.abstractmethod
    def _get_load_message(self):
        pass


class NullLogger(BaseLogger):
    def logging_load(self):
        pass

    def logging_table(self, table_data):
        pass

    def _get_load_message(self):
        return ""


class FileSourceLogger(BaseLogger):
    def _get_load_message(self):
        message = "loading {:s}: format={:s}, path={}".format(
            self._loader.source_type, self._loader.format_name, self._loader.source
        )

        try:
            message += ", encoding={}".format(self._loader.encoding)
        except AttributeError:
            pass

        if self._loader.type_hints:
            message += ", type-hints=({})".format(typehints_to_str(self._loader.type_hints))

        return message


class TextSourceLogger(BaseLogger):
    def _get_load_message(self):
        message = "loading {:s}: format={:s}".format(
            self._loader.source_type, self._loader.format_name
        )

        try:
            message += ", len={}".format(len(self._loader.source))
        except TypeError:
            pass

        try:
            message += ", encoding={}".format(self._loader.encoding)
        except AttributeError:
            pass

        if self._loader.type_hints:
            message += ", type-hints=({})".format(typehints_to_str(self._loader.type_hints))

        return message
