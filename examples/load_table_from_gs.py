#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import pytablewriter as ptw

import pytablereader as ptr


credentials_file = "sample-xxxxxxxxxxxx.json"

loader = ptr.GoogleSheetsTableLoader(credentials_file)
loader.title = "testbook"

for table_data in loader.load():
    print(ptw.dumps_tabledata(table_data))
