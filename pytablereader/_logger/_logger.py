"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc

import dataproperty

from ._null_logger import NullLogger


MODULE_NAME = "pytablereader"

try:
    from loguru import logger

    logger.disable(MODULE_NAME)
except ImportError:
    logger = NullLogger()  # type: ignore


def set_logger(is_enable, propagation_depth=2):
    if is_enable:
        logger.enable(MODULE_NAME)
    else:
        logger.disable(MODULE_NAME)

    if propagation_depth <= 0:
        return

    dataproperty.set_logger(is_enable, propagation_depth - 1)

    try:
        import simplesqlite

        simplesqlite.set_logger(is_enable, propagation_depth - 1)
    except (ImportError, TypeError):
        pass


def set_log_level(log_level):
    # deprecated
    return


def typehints_to_str(type_hints):
    return ", ".join([type_hint.__name__ if type_hint else "none" for type_hint in type_hints])


class LoggerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def logging_load(self):  # pragma: no cover
        pass


class BaseLogger(LoggerInterface):
    def __init__(self, loader):
        self._loader = loader

    def logging_load(self):
        logger.debug(self._get_load_message())

    def logging_table(self, table_data):
        logger.debug(f"loaded tabledata: {table_data}")

    @abc.abstractmethod
    def _get_load_message(self):
        pass


class NullSourceLogger(BaseLogger):
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
            message += f", encoding={self._loader.encoding}"
        except AttributeError:
            pass

        if self._loader.type_hints:
            message += f", type-hints=({typehints_to_str(self._loader.type_hints)})"

        return message


class TextSourceLogger(BaseLogger):
    def _get_load_message(self):
        message = "loading {:s}: format={:s}".format(
            self._loader.source_type, self._loader.format_name
        )

        try:
            message += f", len={len(self._loader.source)}"
        except TypeError:
            pass

        try:
            message += f", encoding={self._loader.encoding}"
        except AttributeError:
            pass

        if self._loader.type_hints:
            message += f", type-hints=({typehints_to_str(self._loader.type_hints)})"

        return message
