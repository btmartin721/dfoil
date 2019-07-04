#!/usr/bin/env python

import argparse
import os
import sys

from tables import *
from data_str import Files

def Get_Arguments():
    """
    Parse command-line arguments. Imported with argparse.
    Returns: object of command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Merges multiple HDF5 files", add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    ## Required Arguments
    required_args.add_argument("-p", "--path",
                                type=str,
                                required=True,
                                help="Path to counts directory; should ONLY contain the relevant HDF5 files")
    required_args.add_argument("-o", "--out",
                                type=str,
                                required=True,
                                help="Specify merged HDF5 filename")
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

    # Append directory of HDF5 files to single HDF5 file
    for filename in os.listdir(path):
        if path.endswith("/"):
            path = path[:-1]
        filename = path + "/" + filename
        with open_file(filename, mode="r") as h5file:
            with open_file(args.out, mode="a") as outfile:
                table1 = h5file.root.files.summary
                summary = table1.row
                if "/all_summary" not in outfile:
                    table2 = outfile.create_table("/", "all_summary", Files, "Appended Summary Table")
                    all_summary = table2.row
                else:
                    table2 = outfile.root.all_summary
                    all_summary = table2.row

                for row in table1.iterrows():
                    all_summary["all_summary"] = row["summary"]
                    all_summary.append()

                table2.flush()

    # Write output to regular text file.
    with open_file(args.out, mode="r") as h5file:
        table = h5file.root.all_summary
        all_summary = table.row
        with open("all.summary.alt.txt", "w") as out:
            for row in table:
                line = list(row["all_summary"].decode().rstrip().split())
                out.write(" ".join(line) + "\n")


    return 0

#===============================================================================
# MAIN

if __name__ == "__main__":
    main()
