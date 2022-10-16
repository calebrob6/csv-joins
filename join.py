#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Caleb Robinson <calebrob6@gmail.com>
#
# Distributed under terms of the MIT license.

import sys
import csv
import argparse


class CSVRows:

    def __init__(self, header, rows, primary_key, file_name):
        self.__header = header
        self.__body = rows
        self.__primary_key = primary_key
        self.__file_name = file_name
        self.__map_primary_key = self.__create_map_primary_key()

    @property
    def header(self):
        return self.__header

    @property
    def body(self):
        return self.__body

    @property
    def primary_key(self):
        return self.__primary_key

    @property
    def primary_key_index(self):
        return self.header.index(self.primary_key)

    @property
    def file_name(self):
        return self.__file_name

    @property
    def map_primary_key(self):
        return self.__map_primary_key

    def check_if_header_has_primary_key_column(self):
        if self.__header_has_primary_key_column():
            raise ValueError(
                f"Error: primary key ({self.primary_key}) not in header "
                f"line of {self.file_name}"
            )

    def check_if_all_values_in_primary_key_column_are_unique(self):
        pk_set = set()
        for row in self.body:
            if row[self.primary_key_index] in pk_set:
                raise ValueError(
                    f"Error: primary key column is not unique in "
                    f"{self.file_name} (duplicate value found: "
                    f"{row[self.primary_key_index]})"
                )
            pk_set.add(row[self.primary_key_index])

    def __create_map_primary_key(self):
        return {r[self.primary_key_index]: i for i, r in enumerate(self.body)}

    def __header_has_primary_key_column(self):
        return self.primary_key not in self.header


class CSVHandler:

    def load_rows_from_csv(self, file_name):
        with open(file_name, "r") as f:
            csv_reader = csv.reader(f)
            return [row for row in csv_reader]

    def save_in_csv(self, output_csv):
        with open(output_csv.file_name, "w") as fp:
            csvWriter = csv.writer(fp)
            csvWriter.writerow(output_csv.header)

            for row in output_csv.body:
                csvWriter.writerow(row)


class CSVRowsBuilder:
    def __init__(self):
        self.__csv_handler = CSVHandler()

    def build_csv_rows(self, file_name, primary_key):
        headers, *rows = self.__csv_handler.load_rows_from_csv(file_name)
        csv_rows = self.__csv_rows_instance(
            headers,
            rows,
            primary_key,
            file_name
        )
        self.__validators(csv_rows)
        return csv_rows

    def __csv_rows_instance(self, headers, rows, primary_key, file_name):
        return CSVRows(headers, rows, primary_key, file_name)

    def __validators(self, csv_rows):
        csv_rows.check_if_header_has_primary_key_column()
        csv_rows.check_if_all_values_in_primary_key_column_are_unique()


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


class Arguments:

    def __init__(self, args):
        self.__verbose = args.verbose
        self.__left_file_name = args.leftFn
        self.__left_primary_key = args.leftPK
        self.__right_file_name = args.rightFn
        self.__right_primary_key = args.rightPK
        self.__output_file_name = args.outputFn
        self.__join_type = args.joinType

    @property
    def verbose(self):
        return self.__verbose

    @property
    def left_file_name(self):
        return self.__left_file_name

    @property
    def left_primary_key(self):
        return self.__left_primary_key

    @property
    def right_file_name(self):
        return self.__right_file_name

    @property
    def right_primary_key(self):
        return self.__right_primary_key

    @property
    def output_file_name(self):
        return self.__output_file_name

    @property
    def join_type(self):
        return self.__join_type


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
