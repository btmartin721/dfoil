#!/bin/bash

mkdir -p counts
names=$1
fasta=$2
outgroup=$3

cat $names | parallel --env outgroup --env fasta './fasta2dfoil_hdf5.py -a <(selectSeqs.pl -f <(echo {} | tr " " $"\n"; cat '$outgroup') '$fasta') --out counts/$(echo {} | tr " " ".").counts.h5 --names $(echo {} | tr " " ","),$(cat '$outgroup')'
