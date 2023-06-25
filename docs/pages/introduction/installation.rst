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
- Python 3.7+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/pytablereader/network/dependencies>`__


Optional Python packages
------------------------------------------------
- ``logging`` extras
    - `loguru <https://github.com/Delgan/loguru>`__: Used for logging if the package installed
- ``excel`` extras
    - `excelrd <https://github.com/thombashi/excelrd>`__
- ``md`` extras
    - `Markdown <https://github.com/Python-Markdown/markdown>`__
- ``mediawiki`` extras
    - `pypandoc <https://github.com/bebraw/pypandoc>`__
- ``sqlite`` extras
    - `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- ``url`` extras
    - `retryrequests <https://github.com/thombashi/retryrequests>`__
- `pandas <https://pandas.pydata.org/>`__
    - required to get table data as a pandas data frame
- `lxml <https://lxml.de/installation.html>`__

Optional packages (other than Python packages)
------------------------------------------------
- ``libxml2`` (faster HTML conversion)
- `pandoc <https://pandoc.org/>`__ (required when loading MediaWiki file)
