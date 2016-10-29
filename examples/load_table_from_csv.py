#!/usr/bin/env python
# encoding: utf-8

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
    print("load from file: {:s}".format(table_data.dumps()))

# load from a csv text ---
loader = pytablereader.CsvTableTextLoader(csv_text)
for table_data in loader.load():
    print("load from text: {:s}".format(table_data.dumps()))
