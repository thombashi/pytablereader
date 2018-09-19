# encoding: utf-8

"""
Unit tests at Windows environments required to invoke from py module,
because of multiprocessing:
https://py.rtfd.io/en/latest/faq.html?highlight=cmdline#issues-with-py-test-multiprocess-and-setuptools
"""

import multiprocessing
import sys

import py


if __name__ == "__main__":
    multiprocessing.freeze_support()
    sys.exit(py.test.cmdline.main())
