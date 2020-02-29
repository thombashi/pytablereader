"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import abc


class LoaderAcceptorInterface(metaclass=abc.ABCMeta):
    """
    An interface class of table loader acceptor.
    """

    @abc.abstractmethod
    def accept(self, loader):  # pragma: no cover
        pass


class LoaderAcceptor(LoaderAcceptorInterface):
    """
    An abstract class of table loader acceptor.
    """

    def __init__(self):
        self._loader = None

    def accept(self, loader):
        self._loader = loader
