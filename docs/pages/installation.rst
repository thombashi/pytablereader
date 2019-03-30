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
- Load from URLs
    - ``pip install pytablereader[url]``
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
- `markdown2 <https://github.com/trentm/python-markdown2>`__
- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `path.py <https://github.com/jaraco/path.py>`__
- `six <https://pypi.org/project/six/>`__
- `tabledata <https://github.com/thombashi/tabledata>`__
- `typepy <https://github.com/thombashi/typepy>`__

Optional Python packages
------------------------------------------------
- `logbook <https://logbook.readthedocs.io/en/stable/>`__
    - Logging using logbook if the package installed
- Excel
    - `xlrd <https://github.com/python-excel/xlrd>`__
- MediaWiki
    - `pypandoc <https://github.com/bebraw/pypandoc>`__
- SQLite
    - `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- URL
    - `requests <http://python-requests.org/>`__
    - `retryrequests <https://github.com/thombashi/retryrequests>`__
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
- `tox <https://testrun.org/tox/latest/>`__
