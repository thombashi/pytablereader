#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from __future__ import unicode_literals
import io

import pytablereader as ptr
import pytablewriter as ptw


print("\n".join([
    "load from URL",
    "==============",
]))

loader = ptr.TableUrlLoader(
    "https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks",
    "html")

with io.open("hoge.rst", "w", encoding=loader.encoding) as f:
    for table_data in loader.load():
        print("{:s}".format(ptw.dump_tabledata(table_data)))
        f.write(ptw.dump_tabledata(table_data))
