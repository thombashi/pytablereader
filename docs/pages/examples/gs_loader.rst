.. _example-gs-table-loader:

Load table data from Google Sheets
-------------------------------------
Following example shows how to extract |TableData| from Google Sheets by using |GoogleSheetsTableLoader| class.

.. code-block:: python
    :caption: Load table data from Google Sheets

    import io

    import pytablereader as ptr
    import pytablewriter as ptw


    loader = ptr.TableUrlLoader(
        "https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks",
        "html")

    writer = ptw.TableWriterFactory.create_from_format_name("rst")
    writer.stream = io.open("load_url_result.rst", "w", encoding=loader.encoding)
    for table_data in loader.load():
        writer.from_tabledata(table_data)
        writer.write_table()

