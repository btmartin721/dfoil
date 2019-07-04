#!/usr/bin/env python

import argparse
import sys

from tables import *
from data_str import Files

def Get_Arguments():
    """
    Parse command-line arguments. Imported with argparse.
    Returns: object of command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Summarizes Results from the dfoil_hdf5.py output"
                                    "ExDFOIL pipeline", add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    ## Required Arguments
    required_args.add_argument("-i", "--infile",
                                type=str,
                                required=True,
                                help="Output from dfoil_hdf5.py")

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

    with open_file(args.infile, mode="r+") as h5file:
        ctab = h5file.root.files.counts
        dtab = h5file.root.files.dfoils
        counts = ctab.row
        dfoils = dtab.row

        clist = list()
        for row in ctab:
            line = list(row["data"].decode().rstrip().split())

            if line[0].startswith("counts/"):
                basename = list(line[0].split("/"))
                taxa = list(basename[1].split("."))
                taxa = list(taxa[:-2])
            else:
                taxa = list(line[0].split("."))
                taxa = taxa[:-2]

            col1 = list(line[3])
            col2 = list(line[4])
            col3 = list(line[6])
            col4 = list(line[10])
            joined = taxa + col4 + col3 + col2 + col1 # Reversed the order
            clist.append([str(v) for v in joined])

        dlist = list()
        for row in dtab:
            line = row["DFOILdata"].decode().rstrip().split()
            introgression = line[31]
            DFOstat = line[10]
            DFOp = line[12]
            DILstat = line[16]
            DILp = line[18]
            DFIstat = line[22]
            DFIp = line[24]
            DOLstat = line[28]
            DOLp = line[30]
            dlist.extend([introgression, DFOstat, DFOp, DILstat, DILp, DFIstat, DFIp, DOLstat, DOLp])

        cCols = " ".join([" ".join(v) for v in clist])
        dCols = " ".join(str(v) for v in dlist)
        joined = cCols + " " + dCols

        if "/files/summary" not in h5file:
            out_table = h5file.create_table("/files", "summary", Files, "Summary Table")
            summary = out_table.row
            summary["summary"] = joined
        else:
            out_table = h5file.root.files.summary
            summary = out_table.row

        summary.append()
        out_table.flush()

        # Debug print statement
        #for row in out_table:
            #print(row["summary"])


    return 0


#===============================================================================
# MAIN

if __name__ == "__main__":
    main()
