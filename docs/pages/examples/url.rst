.. _example-url-table-loader:

Load table data from a web page
-------------------------------------
Following example shows how to extract |TableData| from a web page by using |TableUrlLoader| class.

.. code-block:: python
    :caption: Load table from a web page

    import io

    import pytablereader as ptr
    import pytablewriter as ptw


    loader = ptr.TableUrlLoader(
        "https://en.wikipedia.org/wiki/List_of_unit_testing_frameworks",
        "html")

    writer = ptw.TableWriterFactory.create_from_format_name("rst")
    writer.stream = io.open("load_url_result.rst", "w", encoding=loader.encoding)
    for tabledata in loader.load():
        writer.from_tabledata(tabledata)
        writer.write_table()

.. code-block:: console
    :caption: Output

    $ ./load_table_from_url.py
    $ head load_url_result.rst -n 8
    .. table:: List of unit testing frameworks - Wikipedia_html1

        +---------+-----+------+------------------------+
        |  Name   |xUnit|Source|        Remarks         |
        +=========+=====+======+========================+
        |ABAP Unit|Yes  |[1]   |since SAP NetWeaver 2004|
        +---------+-----+------+------------------------+
