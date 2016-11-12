#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from __future__ import unicode_literals
import io

import pytablereader

print("\n".join([
    "load from URL",
    "==============",
]))

loader = pytablereader.TableUrlLoader(
    "https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks",
    "html")

with io.open("hoge.rst", "w", encoding=loader.encoding) as f:
    for table_data in loader.load():
        print("{:s}".format(table_data.dumps()))
        f.write(table_data.dumps())
