**pytablereader**

.. contents:: Table of Contents
   :depth: 2

Summary
=========
A Python library to load structured table data from files/strings/URL with various data format: CSV / Excel / Google-Sheets / HTML / JSON / LDJSON / LTSV / Markdown / SQLite / TSV.

.. image:: https://badge.fury.io/py/pytablereader.svg
    :target: https://badge.fury.io/py/pytablereader

.. image:: https://img.shields.io/pypi/pyversions/pytablereader.svg
   :target: https://pypi.org/project/pytablereader

.. image:: https://img.shields.io/travis/thombashi/pytablereader/master.svg?label=Linux/macOS
    :target: https://travis-ci.org/thombashi/pytablereader
    :alt: Linux CI test status

.. image:: https://img.shields.io/appveyor/ci/thombashi/pytablereader/master.svg?label=Windows
    :target: https://ci.appveyor.com/project/thombashi/pytablereader/branch/master
    :alt: Windows CI test status

.. image:: https://coveralls.io/repos/github/thombashi/pytablereader/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/pytablereader?branch=master

.. image:: https://img.shields.io/github/stars/thombashi/pytablereader.svg?style=social&label=Star
   :target: https://github.com/thombashi/pytablereader

Features
--------
- Extract structured tabular data from various data format:
    - CSV / Tab separated values (TSV) / Space separated values (SSV)
    - Microsoft Excel :superscript:`TM` file
    - `Google Sheets <https://www.google.com/intl/en_us/sheets/about/>`_
    - HTML
    - JSON
    - `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
    - `Line-delimited JSON(LDJSON) <https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON>`__ / NDJSON / JSON Lines
    - Markdown
    - MediaWiki
    - SQLite database file
- Supported data sources are:
    - Files on a local file system
    - Accessible URLs
    - ``str`` instances
- Loaded table data can be used as:
    - `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html>`__ instance
    - ``dict`` instance

Examples
==========
Load a CSV table
------------------
:Sample Code:
    .. code-block:: python

        import pytablereader as ptr
        import pytablewriter as ptw


        # prepare data ---
        file_path = "sample_data.csv"
        csv_text = "\n".join([
            '"attr_a","attr_b","attr_c"',
            '1,4,"a"',
            '2,2.1,"bb"',
            '3,120.9,"ccc"',
        ])

        with open(file_path, "w") as f:
            f.write(csv_text)

        # load from a csv file ---
        loader = ptr.CsvTableFileLoader(file_path)
        for table_data in loader.load():
            print("\n".join([
                "load from file",
                "==============",
                "{:s}".format(ptw.dump_tabledata(table_data)),
            ]))

        # load from a csv text ---
        loader = ptr.CsvTableTextLoader(csv_text)
        for table_data in loader.load():
            print("\n".join([
                "load from text",
                "==============",
                "{:s}".format(ptw.dump_tabledata(table_data)),
            ]))


:Output:
    .. code-block::

        load from file
        ==============
        .. table:: sample_data

            ======  ======  ======
            attr_a  attr_b  attr_c
            ======  ======  ======
                 1     4.0  a
                 2     2.1  bb
                 3   120.9  ccc
            ======  ======  ======

        load from text
        ==============
        .. table:: csv2

            ======  ======  ======
            attr_a  attr_b  attr_c
            ======  ======  ======
                 1     4.0  a
                 2     2.1  bb
                 3   120.9  ccc
            ======  ======  ======

Get loaded table data as pandas.DataFrame instance
----------------------------------------------------

:Sample Code:
    .. code-block:: python

        import pytablereader as ptr

        loader = ptr.CsvTableTextLoader(
            "\n".join([
                "a,b",
                "1,2",
                "3.3,4.4",
            ]))
        for table_data in loader.load():
            print(table_data.as_dataframe())

:Output:
    .. code-block::

             a    b
        0    1    2
        1  3.3  4.4

For more information
----------------------
More examples are available at 
https://pytablereader.rtfd.io/en/latest/pages/examples/index.html

Installation
============
::

    pip install pytablereader

Some of the formats require additional dependency packages, you can install the dependency packages as follows:

- Excel
    - ``pip install pytablereader[excel]``
- Google Sheets
    - ``pip install pytablereader[gs]``
- Mediawiki
    - ``pip install pytablereader[mediawiki]``
- SQLite
    - ``pip install pytablereader[sqlite]``
- All of the extra dependencies
    - ``pip install pytablereader[all]``


Dependencies
============
Python 2.7+ or 3.4+

Mandatory Python packages
----------------------------------
- `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/>`__
- `DataProperty <https://github.com/thombashi/DataProperty>`__ (Used to extract data types)
- `jsonschema <https://github.com/Julian/jsonschema>`__
- `logbook <https://logbook.readthedocs.io/en/stable/>`__
- `markdown2 <https://github.com/trentm/python-markdown2>`__
- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `path.py <https://github.com/jaraco/path.py>`__
- `requests <http://python-requests.org/>`__
- `six <https://pypi.org/project/six/>`__
- `tabledata <https://github.com/thombashi/tabledata>`__
- `typepy <https://github.com/thombashi/typepy>`__

Optional Python packages
------------------------------------------------
- Excel
    - `xlrd <https://github.com/python-excel/xlrd>`__
- MediaWiki
    - `pypandoc <https://github.com/bebraw/pypandoc>`__
- SQLite
    - `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- `pandas <https://pandas.pydata.org/>`__
    - required to get table data as a pandas data frame
- `simplejson <https://github.com/simplejson/simplejson>`__
- `lxml <https://lxml.de/installation.html>`__

Optional packages (other than Python packages)
------------------------------------------------
- ``libxml2`` (faster HTML conversion)
- `pandoc <https://pandoc.org/>`__ (required when loading MediaWiki file)

Test dependencies
-----------------
- `pytablewriter <https://github.com/thombashi/pytablewriter>`__
- `pytest <https://docs.pytest.org/en/latest/>`__
- `pytest-runner <https://github.com/pytest-dev/pytest-runner>`__
- `responses <https://github.com/getsentry/responses>`__
- `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- `tox <https://testrun.org/tox/latest/>`__

Documentation
===============
https://pytablereader.rtfd.io/

Related Project
=================
- `pytablewriter <https://github.com/thombashi/pytablewriter>`__
    - Tabular data loaded by ``pytablereader`` can be written another tabular data format with ``pytablewriter``.

