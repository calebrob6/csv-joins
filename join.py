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


def do_args(argList, name):
    parser = argparse.ArgumentParser(description=name)

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show output from latex and dvipng commands",
        default=False,
    )
    parser.add_argument("leftFn", type=str, help="Filename of left table")
    parser.add_argument(
        "leftPK",
        type=str,
        help="Name of column to use as the primary key for the left table",
    )
    parser.add_argument(
        "rightFn", type=str, help="Filename of the right table"
    )
    parser.add_argument(
        "rightPK",
        type=str,
        help="Name of column to use as the primary key for the right table",
    )
    parser.add_argument("outputFn", type=str, help="Output filename")
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        action="store",
        dest="joinType",
        choices=["left", "right", "inner", "full"],
        help="Type of join (default is 'left join')",
        default="left",
    )

    return parser.parse_args(argList)


def main():

    args = do_args(sys.argv[1:], "CSV join script")

    arguments = Arguments(args)
    # -------------------------------------------------------------------------
    # Load the left data file
    # -------------------------------------------------------------------------

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
    output_rows = []


    if arguments.join_type == "left":

        # Iterate through each row in the left table, try to find the matching
        # row in the right table if the matching row doesn't exist, then fill
        # with 'null's, if it does, then copy it over
        for leftRow in left_csv.body:
            leftRowPK = leftRow[left_csv.primary_key_index]
            rightRow = None
            if leftRowPK in right_csv.map_primary_key:
                rightRow = right_csv.body[right_csv.map_primary_key[leftRowPK]]
            else:
                rightRow = ["null"] * len(right_csv.header)

            # csvWriter.writerow(leftRow + rightRow)
            output_rows.append(leftRow + rightRow)
    elif arguments.join_type == "right":

        # Similar to 'left' case
        for rightRow in right_csv.body:
            rightRowPK = rightRow[right_csv.primary_key_index]
            leftRow = None
            if rightRowPK in left_csv.map_primary_key:
                leftRow = left_csv.body[left_csv.map_primary_key[rightRowPK]]
            else:
                leftRow = ["null"] * len(left_csv.header)

            # csvWriter.writerow(leftRow + rightRow)
            output_rows.append(leftRow + rightRow)
    elif arguments.join_type == "inner":
        # This join will only write rows for primary keys in the intersection
        # of the two primary key sets
        leftKeySet = set(left_csv.map_primary_key.keys())
        rightKeySet = set(right_csv.map_primary_key.keys())

        newKeys = leftKeySet & rightKeySet

        for keyVal in newKeys:
            leftRow = left_csv.body[left_csv.map_primary_key[keyVal]]
            rightRow = right_csv.body[right_csv.map_primary_key[keyVal]]

            # csvWriter.writerow(leftRow + rightRow)
            output_rows.append(leftRow + rightRow)
    elif arguments.join_type == "full":
        # This join will only write rows for primary keys in the union of the
        # two primary key sets
        leftKeySet = set(left_csv.map_primary_key.keys())
        rightKeySet = set(right_csv.map_primary_key.keys())

        newKeys = leftKeySet | rightKeySet

        for keyVal in newKeys:
            leftRow = None
            if keyVal in left_csv.map_primary_key:
                leftRow = left_csv.body[left_csv.map_primary_key[keyVal]]
            else:
                leftRow = ["null"] * len(left_csv.header)

            rightRow = None
            if keyVal in right_csv.map_primary_key:
                rightRow = right_csv.body[right_csv.map_primary_key[keyVal]]
            else:
                rightRow = ["null"] * len(right_csv.header)

            # csvWriter.writerow(leftRow + rightRow)
            output_rows.append(leftRow + rightRow)
    else:
        raise Exception("This shouldn't happen")


    output_csv = CSVRows(
        output_header,
        output_rows,
        'a',
        arguments.output_file_name
    )

    csv_handler = CSVHandler()

    csv_handler.save_in_csv(output_csv)

if __name__ == "__main__":
    main()
