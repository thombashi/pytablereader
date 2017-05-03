#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import pytablereader as ptr
import pytablewriter as ptw


credentials_file = "sample-xxxxxxxxxxxx.json"

loader = ptr.GoogleSheetsTableLoader(credentials_file)
loader.title = "testbook"

for tabledata in loader.load():
    print(ptw.dump_tabledata(tabledata))
