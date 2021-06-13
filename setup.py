#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os.path

import setuptools


MODULE_NAME = "pytablereader"
REPOSITORY_URL = f"https://github.com/thombashi/{MODULE_NAME:s}"
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

pkg_info = {}


def get_release_command_class():
    try:
        from releasecmd import ReleaseCommand
    except ImportError:
        return {}

    return {"release": ReleaseCommand}


with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)

with open("README.rst", encoding=ENCODING) as fp:
    long_description = fp.read()

with open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding=ENCODING) as f:
    summary = f.read().strip()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

setuptools_require = ["setuptools>=38.3.0"]
excel_requires = ["excelrd>=2.0.2"]

markdown_requires = ["Markdown>=2.6.6,<4"]
mediawiki_requires = ["pypandoc"]
sqlite_requires = ["SimpleSQLite>=1.2,<2"]
gs_requires = ["gspread", "oauth2client", "pyOpenSSL"] + sqlite_requires
logging_requires = ["loguru>=0.4.1,<1"]
url_requires = ["retryrequests>=0.1,<1"]
optional_requires = ["simplejson>=3.8.1,<4"]
tests_requires = frozenset(
    tests_requires
    + excel_requires
    + markdown_requires
    + mediawiki_requires
    + sqlite_requires
    + url_requires
)

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,
    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=summary,
    include_package_data=True,
    keywords=[
        "table",
        "reader",
        "pandas",
        "CSV",
        "Excel",
        "HTML",
        "JSON",
        "LTSV",
        "Markdown",
        "MediaWiki",
        "TSV",
        "SQLite",
    ],
    license=pkg_info["__license__"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(exclude=["test*"]),
    project_urls={
        "Documentation": f"https://{MODULE_NAME:s}.rtfd.io/",
        "Source": REPOSITORY_URL,
        "Tracker": f"{REPOSITORY_URL:s}/issues",
        "Changes": f"{REPOSITORY_URL:s}/releases",
    },
    python_requires=">=3.6",
    install_requires=setuptools_require + install_requires,
    setup_requires=setuptools_require,
    extras_require={
        "all": set(
            excel_requires
            + gs_requires
            + logging_requires
            + markdown_requires
            + mediawiki_requires
            + sqlite_requires
            + url_requires
        ),
        "excel": excel_requires,
        "gs": gs_requires,
        "logging": logging_requires,
        "md": markdown_requires,
        "mediawiki": mediawiki_requires,
        "url": url_requires,
        "sqlite": sqlite_requires,
        "test": tests_requires,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
    ],
    cmdclass=get_release_command_class(),
)
