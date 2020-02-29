#!/usr/bin/env python3

import pytablewriter as ptw

import pytablereader as ptr


loader = ptr.TableUrlLoader(
    "https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks",
    "html")

writer = ptw.TableWriterFactory.create_from_format_name("rst")
writer.stream = open("load_url_result.rst", "w", encoding=loader.encoding)
for table_data in loader.load():
    writer.from_tabledata(table_data)
    writer.write_table()
