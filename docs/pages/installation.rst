Installation
============

Install from PyPI
------------------------------
::

    pip install pytablereader

Some of the formats require additional dependency packages, you can install the dependency packages as follows:

- Excel
    - ``pip install pytablereader[excel]``
- Google Sheets
    - ``pip install pytablereader[gs]``
- Markdown
    - ``pip install pytablereader[md]``
- Mediawiki
    - ``pip install pytablereader[mediawiki]``
- SQLite
    - ``pip install pytablereader[sqlite]``
- Load from URLs
    - ``pip install pytablereader[url]``
- All of the extra dependencies
    - ``pip install pytablereader[all]``

Install from PPA (for Ubuntu)
------------------------------
::

    sudo add-apt-repository ppa:thombashi/ppa
    sudo apt update
    sudo apt install python3-pytablereader


Dependencies
============
Python 3.5+

Mandatory Python packages
----------------------------------
- `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/>`__
- `DataProperty <https://github.com/thombashi/DataProperty>`__ (Used to extract data types)
- `jsonschema <https://github.com/Julian/jsonschema>`__
- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `path <https://github.com/jaraco/path>`__
- `tabledata <https://github.com/thombashi/tabledata>`__
- `typepy <https://github.com/thombashi/typepy>`__

Optional Python packages
------------------------------------------------
- `loguru <https://github.com/Delgan/loguru>`__
    - Used for logging if the package installed
- Excel
    - `excelrd <https://github.com/thombashi/excelrd>`__
- Markdown
    - `markdown2 <https://github.com/trentm/python-markdown2>`__
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
- `responses <https://github.com/getsentry/responses>`__
- `tox <https://testrun.org/tox/latest/>`__
