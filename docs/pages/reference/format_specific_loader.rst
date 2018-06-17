Format Specific Table Loader Classes
--------------------------------------------

TableLoader class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablereader.interface.TableLoader
    :inherited-members:
    :show-inheritance:


CSV Loader Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CSV Table Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.csv.core.CsvTableLoader
    :inherited-members:

CSV File Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.CsvTableFileLoader
    :inherited-members:
    :show-inheritance:

CSV Text Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.CsvTableTextLoader
    :inherited-members:
    :exclude-members: source_type,get_format_key,make_table_name
    :show-inheritance:


HTML Loader Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HTML File Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.HtmlTableFileLoader
    :inherited-members:

HTML Text Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.HtmlTableTextLoader
    :inherited-members:


JSON Loader Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Json File Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.JsonTableFileLoader
    :inherited-members:

Json Text Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.JsonTableTextLoader
    :inherited-members:

Line-delimited Json File Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.JsonLinesTableFileLoader
    :inherited-members:

Line-delimited Json Text Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.JsonLinesTableTextLoader
    :inherited-members:


LTSV Loader Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LTSV File Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.LtsvTableFileLoader
    :inherited-members:
    :show-inheritance:

LTSV Text Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.LtsvTableTextLoader
    :inherited-members:
    :exclude-members: source_type,get_format_key,make_table_name
    :show-inheritance:


Markdown Loader Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Markdown File Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.MarkdownTableFileLoader
    :inherited-members:

Markdown Text Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.MarkdownTableTextLoader
    :inherited-members:


MediaWiki Loader Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MediaWiki File Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.MediaWikiTableFileLoader
    :inherited-members:

MediaWiki Text Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.MediaWikiTableTextLoader
    :inherited-members:


Spread Sheet Loader Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Excel File Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.ExcelTableFileLoader
    :inherited-members:

Google Sheets Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.GoogleSheetsTableLoader
    :inherited-members:


Database Loader Classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SQLite File Loader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: pytablereader.SqliteFileLoader
    :inherited-members:
