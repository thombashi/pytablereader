"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


from typing import Optional, Sequence

import typepy

from ..factory import TableTextLoaderFactory
from ._base import TableLoaderManager


class TableTextLoader(TableLoaderManager):
    """
    Loader class to loading tables from URL.

    :param str url: URL to load.
    :param str format_name: Data format name to load.
        Supported formats can be get by :py:meth:`.get_format_names`
    :param dict proxies: http/https proxy information.

        .. seealso::
            `requests proxies <http://docs.python-requests.org/en/master/user/advanced/#proxies>`__

    :raises pytablereader.LoaderNotFoundError:
        |LoaderNotFoundError_desc| loading the URL.

    .. py:method:: load

        Load tables from text as ``format_name`` format.

        :return: Loaded table data iterator.
        :rtype: |TableData| iterator

        .. seealso::
            * :py:meth:`pytablereader.factory.TableTextLoaderFactory.create_from_format_name`
            * :py:meth:`pytablereader.factory.TableTextLoaderFactory.create_from_path`
    """

    def __init__(
        self, source: str, format_name: str, encoding: Optional[str] = None, type_hint_rules=None
    ) -> None:
        loader_factory = TableTextLoaderFactory(source, encoding)

        if typepy.is_null_string(format_name):
            raise ValueError("requie format_name")

        loader = loader_factory.create_from_format_name(format_name)
        loader.type_hint_rules = type_hint_rules

        super().__init__(loader)

    @classmethod
    def get_format_names(cls) -> Sequence[str]:
        """
        :return:
            Available format names. These names can use by
            :py:class:`.TableTextLoader` class constructor.
        :rtype: list

        :Example:
            .. code:: python

                >>> from pytablereader import TableTextLoader
                >>> for format_name in TableTextLoader.get_format_names():
                ...     print(format_name)
                ...
                csv
                excel
                html
                json
                json_lines
                jsonl
                ldjson
                ltsv
                markdown
                mediawiki
                ndjson
                sqlite
                ssv
                tsv
        """

        return TableTextLoaderFactory("dummy").get_format_names()
