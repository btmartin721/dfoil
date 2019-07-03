#!/usr/bin/env python

import argparse
import os
import re
import sys

from tables import *

def Get_Arguments():
    """
    Parse command-line arguments. Imported with argparse.
    Returns: object of command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Summarizes Results from the "
                                    "ExDFOIL pipeline", add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    ## Required Arguments
    required_args.add_argument("-p", "--path",
                                type=str,
                                required=True,
                                help="Path to counts directory; no slash at end")
    required_args.add_argument("-o", "--out",
                                type=str,
                                required=True,
                                help="Output HDF5 table")



    optional_args.add_argument("-h", "--help",
                                action="help",
                                help="Displays this help menu")

    # Call help if no command-line arguments
    if len(sys.argv)==1:
        print("\nExiting because no command-line options were called.\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    return args

def main():

    args = Get_Arguments()

    path=str(args.path)

    for filename in os.listdir(path):
        with open_file(filename, mode="r") as h5file:
            with open_file(args.out, mode="a") as outfile:
                summary = h5file.root.summary
                all_summary = h5file.copy_node("/", name="summary", \
                        newparent=outfile.root, newname="all_summary")

                all_summary.append(summary[:])

    with open_file(args.out, mode="r") as h5file:
        table = h5file.root.files.all_summary
        summary = table.row

        for row in table:
            print(row["all_summary"])

    return 0

#===============================================================================
# MAIN

if __name__ == "__main__":
    main()
