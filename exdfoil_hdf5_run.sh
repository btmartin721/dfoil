#!/bin/bash

picked=$1
fasta=$2
outgroup=$3
countsDIR=$4
outTable=$5
sampleinfo=$6

# Step 1: Generates counts files from fasta; requires selectSeqs.pl script from ExDFOIL package
# $picked is the output from DFOIL_picker.R (see ExDFOIL package)
# $fasta is the full fasta file
# $outgroup is just file containing the sample ID for one outgroup sample

echo "Beginning fasta2foiler_hdf5.sh...\n\n"

fasta2foiler_hdf5.sh $picked $fasta $outgroup

echo "\n...DONE! Finished with fasta2foiler_hdf5.sh\n\n"

echo "\nBeginning dfoiler_alt_hdf5.sh...\n\n"

# Step 2: runs dfoil.py with GNU parallel
dfoiler_alt_hdf5.sh

echo "\n...DONE! Finised with dfoiler_alt_hdf5.sh\n\n"

# Step 3 (optional): Calculates summary statistics from dfoil_hdf5.py output; not necessary
# dfoil_analyze_hdf5.sh

echo "\nBeginning summarize_alt_hdf5.py...\n\n"

# Step 4: Runs summarize_alt_hdf5.py with GNU parallel
runSummary.sh 

echo "...DONE! Finished with summarize_alt_hdf5.py\n\n"


echo "Beginning merging of HDF5 files...\n\n"
# Step 5: Merges all the HDF5 files into a single HDF5 file
# First argument is produced during Step 4. Second one is the sample info (see ExDFOIL README)
merge_hdf5.py -p $countsDIR -o $outTable

echo "...DONE! Finished with merge\n\n"

echo "Beginning associate.sh...\n\n"

associate.sh all.summary.alt.txt $sampleinfo

echo "...DONE! All finished!"

