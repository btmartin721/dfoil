#!/bin/bash
mkdir -p dfoil
mkdir -p precheck
find ./counts/ -type f -name '*.tab.h5' | parallel python dfoil_hdf5.py -H --mode dfoilalt --infile {} --out dfoil/{/.}.dfoil_alt
