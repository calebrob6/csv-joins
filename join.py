#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import sys
import argparse

from csv_rows import CSVRows
from csv_handler import CSVHandler
from csv_rows_builder import CSVRowsBuilder
from arguments import Arguments
from join_strategies import JoinFactory


def configure_arguments(arguments, name):
    parser = argparse.ArgumentParser(description=name)

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show output from latex and dvipng commands",
        default=False,
    )
    parser.add_argument(
        "left_file_name",
        type=str,
        help="Filename of left table"
    )
    parser.add_argument(
        "left_primary_key",
        type=str,
        help="Name of column to use as the primary key for the left table",
    )
    parser.add_argument(
        "right_file_name",
        type=str,
        help="Filename of the right table"
    )
    parser.add_argument(
        "right_primary_key",
        type=str,
        help="Name of column to use as the primary key for the right table",
    )
    parser.add_argument("output_file_name", type=str, help="Output filename")
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        action="store",
        dest="join_strategy",
        choices=["left", "right", "inner", "full"],
        help="Type of join (default is 'left join')",
        default="left",
    )

    return parser.parse_args(arguments)


class Main:

    def __call__(self, arguments):
        builder = CSVRowsBuilder()

        left_csv = builder.build_csv_rows(
            arguments.left_file_name,
            arguments.left_primary_key
        )

        # -------------------------------------------------------------------------
        # Load the right data file
        # -------------------------------------------------------------------------

        right_csv = builder.build_csv_rows(
            arguments.right_file_name,
            arguments.right_primary_key
        )

        # -------------------------------------------------------------------------
        # Write output file
        # -------------------------------------------------------------------------

        output_header = left_csv.header + right_csv.header

        factory = JoinFactory()

        strategy = factory.join_strategy(arguments.join_strategy)

        output_rows = strategy.join(left_csv, right_csv)

        output_csv = CSVRows(
            output_header,
            output_rows,
            'a',
            arguments.output_file_name
        )

        csv_handler = CSVHandler()

        csv_handler.save_in_csv(output_csv)


if __name__ == "__main__":
    args = configure_arguments(sys.argv[1:], "CSV join script")
    arguments = Arguments(args)

    main = Main()
    main(arguments)
