pytablereader
=============

.. image:: https://badge.fury.io/py/pytablereader.svg
    :target: https://badge.fury.io/py/pytablereader

.. image:: https://img.shields.io/pypi/pyversions/pytablereader.svg
   :target: https://pypi.python.org/pypi/pytablereader

.. image:: https://img.shields.io/travis/thombashi/pytablereader/master.svg?label=Linux
    :target: https://travis-ci.org/thombashi/pytablereader
    :alt: Linux CI test status

.. image:: https://img.shields.io/appveyor/ci/thombashi/pytablereader/master.svg?label=Windows
    :target: https://ci.appveyor.com/project/thombashi/pytablereader/branch/master
    :alt: Windows CI test status

.. image:: https://coveralls.io/repos/github/thombashi/pytablereader/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/pytablereader?branch=master

Summary
-------

pytablereader is a python library to load structured table data from files/URL with various data format: CSV/HTML/JSON/Markdown/MediaWiki/MediaWiki/Excel.

Feature
-------

- Extract structured table data from various data format:
    - CSV file/text
    - Microsoft Excel :superscript:`TM` file
    - HTML file/text
    - JSON file/text
    - Markdown file/text
    - MediaWiki file/text
- Supported data sources to read:
    - Files
    - URL

Examples
========

Load a CSV table
----------------


.. code:: python

    from __future__ import print_function
    import pytablereader

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
    loader = pytablereader.CsvTableFileLoader(file_path)
    for table_data in loader.load():
        print("\n".join([
            "load from file",
            "==============",
            "{:s}".format(table_data.dumps()),
        ]))

    # load from a csv text ---
    loader = pytablereader.CsvTableTextLoader(csv_text)
    for table_data in loader.load():
        print("\n".join([
            "load from text",
            "==============",
            "{:s}".format(table_data.dumps()),
        ]))


.. code::

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


For more information
--------------------

More examples are available at 
http://pytablereader.readthedocs.org/en/latest/pages/examples/index.html

Installation
============

::

    pip install pytablereader


Dependencies
============

Python 2.7+ or 3.3+

Mandatory Python packages
----------------------------------
- `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/>`__
- `DataPropery <https://github.com/thombashi/DataProperty>`__ (Used to extract data types)
- `jsonschema <https://github.com/Julian/jsonschema>`__
- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `path.py <https://github.com/jaraco/path.py>`__
- `requests <http://python-requests.org/>`__
- `six <https://pypi.python.org/pypi/six/>`__
- `xlrd <https://github.com/python-excel/xlrd>`__

Optional Python packages
------------------------------------------------
- `pypandoc <https://github.com/bebraw/pypandoc>`__
    - required when loading MediaWiki file
- `pandas <http://pandas.pydata.org/>`__
    - required to get table data as a pandas data frame

Optional packages (other than Python packages)
------------------------------------------------
- `lxml <http://lxml.de/installation.html>`__ (faster HTML convert if installed)
- `pandoc <http://pandoc.org/>`__ (required when loading MediaWiki file)


Test dependencies
-----------------
-  `pytest <http://pytest.org/latest/>`__
-  `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
-  `tox <https://testrun.org/tox/latest/>`__
-  `XlsxWriter <http://xlsxwriter.readthedocs.io/>`__

Documentation
=============

http://pytablereader.readthedocs.org/en/latest/

Related Project
===============

- `pytablewriter <https://github.com/thombashi/pytablewriter>`__
    - Loaded table data with ``pytablereader`` can write another table format by ``pytablewriter``.

