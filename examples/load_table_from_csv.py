#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

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
