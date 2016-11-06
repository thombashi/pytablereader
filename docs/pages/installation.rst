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
