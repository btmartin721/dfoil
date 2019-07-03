#!/bin/bash
mkdir -p dfoil
mkdir -p precheck
find ./counts/ -type f -name '*.counts' | parallel python dfoil.py --mode dfoilalt --infile {} --out dfoil/{/.}.dfoil_alt ">" precheck/{/.}.precheck_alt
