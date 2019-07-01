#!/bin/bash

find ./counts/ -type f -name '*.tab.h5' | parallel python dfoil_analyze_hdf5.py {} -H
