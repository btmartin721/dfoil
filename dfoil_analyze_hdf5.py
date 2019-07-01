#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DFOIL: Directional introgression testing a five-taxon phylogeny
dfoil_analyze: Given a dfoil output file, gives summary statistics to stdout
James B. Pease
http://www.github.com/jbpease/dfoil
"""

from __future__ import print_function
import sys
import argparse
from numpy import mean, percentile, var, std
from tables import *

from data_str import *
from dfoil_hdf5 import make_header


_LICENSE = """
If you use this software please cite:
Pease JB and MW Hahn. 2015.
"Detection and Polarization of Introgression in a Five-taxon Phylogeny"
Systematic Biology. 64 (4): 651-662.
http://www.dx.doi.org/10.1093/sysbio/syv023

This file is part of DFOIL.

DFOIL is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DFOIL is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DFOIL.  If not, see <http://www.gnu.org/licenses/>.
"""
def printlist(entry, delim="\t", ndigits=3):
    """Print a tab-separated list of items
        Arguments:
            entry: list of elements in line
            delim: field delimeter (default=\t)
    """
    decstring = "{0:." + str(ndigits) + "f}"
    newlist = []
    for elem in entry:
        try:
            if int(elem) == elem:
                newlist.append(int(elem))
            else:
                raise ValueError
        except ValueError as errstr:
            try:
                newlist.append(decstring.format(elem))
            except ValueError as errstr:
                newlist.append(str(elem))
    print(delim.join(["{}".format(x) for x in newlist]))

def writelist(myhdf5file, entry, delim="\t", ndigits=3):
    """Print a tab-separated list of items
        Arguments:
            entry: list of elements in line
            delim: field delimeter (default=\t)
    """
    decstring = "{0:." + str(ndigits) + "f}"
    newlist = []
    for elem in entry:
        try:
            if int(elem) == elem:
                newlist.append(int(elem))
            else:
                raise ValueError
        except ValueError as errstr:
            try:
                newlist.append(decstring.format(elem))
            except ValueError as errstr:
                newlist.append(str(elem))
    myhdf5file["analyzed"] = delim.join(["{}".format(x) for x in newlist])
    myhdf5file.append()
    return myhdf5file

def generate_argparser():
    parser = argparse.ArgumentParser(
        prog="dfoil_analyze.py",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=_LICENSE)
    parser.add_argument("infile", help="dfoil output file")
    parser.add_argument("--ndigits", type=int, default=3,
                        help="number of decimal places")
    parser.add_argument("--hdf5", "-H", action="store_true", default=False,
                        help="Append output to HDF5 file")
    return parser


def main(arguments=None):
    """Main method"""
    arguments = arguments if arguments is not None else sys.argv[1:]
    parser = generate_argparser()
    args = parser.parse_args(args=arguments)
    if args.hdf5:
        dfo = [[], [], []]
        dil = [[], [], []]
        dfi = [[], [], []]
        dol = [[], [], []]
        headers = []
        introg_call = {}
        with open_file(args.infile, mode="r+") as h5file:
            table = h5file.root.files.dfoils
            dfoils = table.row
            for row in table:
                tmpline = row["DFOILheader"].decode()
                headers = tmpline[1:].rstrip().split("\t")
                entry = row["DFOILdata"].decode().split()
                if len(entry) < 32:
                    continue
                introg_call[entry[31]] = introg_call.get(entry[31], 0) + 1
                for name, dstat in (('DFO', dfo), ('DIL', dil),
                                    ('DFI', dfi), ('DOL', dol)):
                    chisq = entry[headers.index(name + '_chisq')]
                    dval = entry[headers.index(name + '_stat')]
                    pval = entry[headers.index(name + '_Pvalue')]
                    if float(chisq) != 0:
                        if dval != 'na':
                            dstat[0].append(float(dval))
                        if chisq != 'na':
                            dstat[1].append(float(chisq))
                        if pval != 'na':
                            dstat[2].append(float(pval))
            statobj = (('DFO', dfo), ('DIL', dil), ('DFI', dfi), ('DOL', dol))
            statfields = ['D', 'chisq', 'Pvalue']

            if "/files/analyzed" not in h5file:
                out_table = h5file.create_table("/files", "analyzed", Files, "Analyzed DFOIL Table")
                analyzed = out_table.row
            else:
                out_table = h5file.root.files.analyzed
                analyzed = out_table.row

            analyzed["analyzed"] = "\n# DFOIL component summary statistics:\n"
            analyzed.append()
            for name, dstat in statobj:
                analyzed["analyzed"] = "\t".join([
                    "stat", "min", "mean", "max",
                    "5%ile", "25%ile", "50%ile", "75%ile", "95%ile",
                    "var", "sd  ", 'ab<0.01', '>0  ',
                    '<0.05', 'cr0.5', 'cr0.05', 'cr0.01',
                    ])
                for i in range(len(dstat)):
                    total = len(dstat[i])
                    if len(dstat[i]) == 0:
                        entry = [name if i == 0 else statfields[i]] + ["na"] * 16
                    else:
                        entry = (
                            [(name if i == 0 else statfields[i]),
                             min(dstat[i]), mean(dstat[i]), max(dstat[i])] +
                            [percentile(dstat[i], x) for x in (5, 25, 50, 75, 95)] +
                            [var(dstat[i]), std(dstat[i]),
                             float(sum([int(abs(x) <= 0.01)
                                        for x in dstat[i]])) / total,
                             float(sum([int(x > 0) for x in dstat[i]])) / total,
                             float(sum([int(x <= 0.05) for x in dstat[i]])) / total,
                             float(sum([int(x >= 0.46) for x in dstat[i]])) / total,
                             float(sum([int(x >= 3.84) for x in dstat[i]])) / total,
                             float(sum([int(x >= 6.64) for x in dstat[i]])) / total])
                    analyzed = writelist(analyzed, entry, ndigits=args.ndigits)
            analyzed["analyzed"] = "\n# Introgression Calls:\n"
            analyzed.append()
            for (key, value) in iter(introg_call.items()):
                analyzed["analyzed"] = "(" + str(key) + "," + str(value) + ")"
            analyzed.append()
            out_table.flush()
            # Debug print statement
            #for row in out_table:
                #print(row["analyzed"].decode())
        return ''

    elif not args.hdf5:
        dfo = [[], [], []]
        dil = [[], [], []]
        dfi = [[], [], []]
        dol = [[], [], []]
        headers = []
        introg_call = {}
        with open(args.infile) as infile:
            for line in infile:
                if line[0] == '#':
                    headers = line[1:].rstrip().split("\t")
                else:
                    entry = line.split()
                    if len(entry) < 32:
                        continue
                    introg_call[entry[31]] = introg_call.get(entry[31], 0) + 1
                    for name, dstat in (('DFO', dfo), ('DIL', dil),
                                        ('DFI', dfi), ('DOL', dol)):
                        chisq = entry[headers.index(name + '_chisq')]
                        dval = entry[headers.index(name + '_stat')]
                        pval = entry[headers.index(name + '_Pvalue')]
                        if float(chisq) != 0:
                            if dval != 'na':
                                dstat[0].append(float(dval))
                            if chisq != 'na':
                                dstat[1].append(float(chisq))
                            if pval != 'na':
                                dstat[2].append(float(pval))
        statobj = (('DFO', dfo), ('DIL', dil), ('DFI', dfi), ('DOL', dol))
        statfields = ['D', 'chisq', 'Pvalue']
        print("\n# DFOIL component summary statistics:\n")
        for name, dstat in statobj:
            print("\t".join([
                "stat", "min", "mean", "max",
                "5%ile", "25%ile", "50%ile", "75%ile", "95%ile",
                "var", "sd  ", 'ab<0.01', '>0  ',
                '<0.05', 'cr0.5', 'cr0.05', 'cr0.01',
                ]))
            for i in range(len(dstat)):
                total = len(dstat[i])
                if len(dstat[i]) == 0:
                    entry = [name if i == 0 else statfields[i]] + ["na"] * 16
                else:
                    entry = (
                        [(name if i == 0 else statfields[i]),
                         min(dstat[i]), mean(dstat[i]), max(dstat[i])] +
                        [percentile(dstat[i], x) for x in (5, 25, 50, 75, 95)] +
                        [var(dstat[i]), std(dstat[i]),
                         float(sum([int(abs(x) <= 0.01)
                                    for x in dstat[i]])) / total,
                         float(sum([int(x > 0) for x in dstat[i]])) / total,
                         float(sum([int(x <= 0.05) for x in dstat[i]])) / total,
                         float(sum([int(x >= 0.46) for x in dstat[i]])) / total,
                         float(sum([int(x >= 3.84) for x in dstat[i]])) / total,
                         float(sum([int(x >= 6.64) for x in dstat[i]])) / total])
                printlist(entry, ndigits=args.ndigits)
        print("\n# Introgression Calls:\n")
        for (key, value) in iter(introg_call.items()):
            print(key, value)
        return ''


if __name__ == "__main__":
    main()
