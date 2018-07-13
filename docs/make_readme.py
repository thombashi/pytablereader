#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import sys

import readmemaker
from path import Path


PROJECT_NAME = "pytablereader"
OUTPUT_DIR = ".."


def write_examples(maker):
    maker.set_indent_level(0)
    maker.write_chapter("Examples")

    examples_root = Path("pages").joinpath("examples")
    maker.inc_indent_level()

    maker.write_chapter("Load a CSV table")
    maker.write_file(examples_root.joinpath("load_csv.txt"))

    maker.write_chapter("Get loaded table data as pandas.DataFrame instance")
    maker.write_file(examples_root.joinpath("as_dataframe.txt"))

    maker.write_chapter("For more information")
    maker.write_line_list(
        [
            "More examples are available at ",
            "http://{:s}.rtfd.io/en/latest/pages/examples/index.html".format(PROJECT_NAME),
        ]
    )


def main():
    maker = readmemaker.ReadmeMaker(PROJECT_NAME, OUTPUT_DIR, is_make_toc=True)

    maker.write_chapter("Summary")
    maker.write_introduction_file("summary.txt")
    maker.write_introduction_file("badges.txt")
    maker.write_introduction_file("feature.txt")

    write_examples(maker)

    maker.write_file(maker.doc_page_root_dir_path.joinpath("installation.rst"))

    maker.set_indent_level(0)
    maker.write_chapter("Documentation")
    maker.write_line_list(["http://{:s}.rtfd.io/".format(PROJECT_NAME)])

    maker.write_chapter("Related Project")
    maker.write_line_list(
        [
            "- `pytablewriter <https://github.com/thombashi/pytablewriter>`__",
            "    - Tabular data loaded by ``pytablereader`` can be written "
            "another tabular data format with ``pytablewriter``.",
        ]
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
