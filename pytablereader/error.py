"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


class ValidationError(Exception):
    """
    Exception raised when data is not properly formatted.
    """


class PathError(Exception):
    """
    Base path exception class.
    """


class InvalidFilePathError(PathError):
    """
    Exception raised when invalid file path used.

    TODO: rename the error class
    """


class UrlError(PathError):
    """
    Exception raised when invalid URL used.
    """


class OpenError(IOError):
    """
    Exception raised when failed to open a file.
    """


class APIError(Exception):
    """
    Exception raised when failed to execute API requests.
    """


class LoaderNotFoundError(Exception):
    """
    Exception raised when loader not found.
    """


class PypandocImportError(ImportError):
    """
    Exception raised when import error occurred with pypandoc package.
    """


try:
    import requests

    class HTTPError(requests.RequestException):
        """
        An HTTP error occurred.

        .. seealso::

            http://docs.python-requests.org/en/master/api/#exceptions
        """

    class ProxyError(requests.exceptions.ProxyError):
        """
        A proxy error occurred.

        .. seealso::

            http://docs.python-requests.org/en/master/_modules/requests/exceptions/
        """


except ImportError:

    class HTTPError(Exception):
        """
        An HTTP error occurred.
        """

    class ProxyError(Exception):
        """
        A proxy error occurred.
        """
