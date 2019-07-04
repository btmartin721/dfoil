# dfoil_hdf5

**Software for detection of introgression in a five-taxon symmetric phylogeny** 

## Citation Information

If you use this program, please cite:
```
James B Pease, Matthew W. Hahn. 2015.
"Detection and Polarization of Introgression in a Five-taxon Phylogeny" 
Systematic Biology. 64 (4): 651-662.
http://www.dx.doi.org/10.1093/sysbio/syv023
doi: 10.1093/sysbio/syv023
```

Please also include a link to [http://www.github.com/jbpease/dfoil](http://www.github.com/jbpease/dfoil)

## Manual

See the manual for dfoil (https://github.com/jbpease/dfoil/blob/master/dfoil.pdf).
And also the ExDFOIL README (https://github.com/SheaML/ExDFOIL)

## License

This file is part of dfoil.

dfoil is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

dfoil is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with Foobar.  If not, see (http://www.gnu.org/licenses/).

# HDF5 Updates

If you need info about the specific input file format, see the ExDFOIL GitHub page.

## Dependencies  

pytables  
numpy  
Python 2 or 3 (tested with v3.7.3)  
GNU parallel  
All the requirements of the original dfoil.py and ExDFOIL scripts.  

I included a conda environment file (environment.yml) that you can use to install the dependencies. But admittedly it hasn't been tested with a new environment.  

## Purpose for modifying / writing code  

My main goal here was to make [ExDFOIL](https://github.com/SheaML/ExDFOIL) more efficient given that in large RADseq datasets it will write millions of files to disk (my dataset tried to write 6 million files X 4).   

To do so, I have modified the original [dfoil](http://www.github.com/jbpease/dfoil) scripts to write to HDF5 files using PyTables.  Also, I have drastically reduced the number of files written to disk (down to 25% of what it was) by writing the ExDFOIL output from the three pipeline steps (\*.counts, \*.dfoil_alt, and \*.summary_alt) to a single HDF5 file as separate tables. It still writes one file per test because I couldn't think of a better way to parallelize it than GNU parallel.  

## exdfoil_hdf5_run.sh  

Here is a script to run the whole pipeline. There are several command-line arguments. See comments inside the script.  

## fasta2dfoil_hdf5.py  
fasta2dfoil_hdf5.py now saves output as an HDF5 table if the -H,--hdf5 option is used. The original script runs if -H flag is not provided.    

Added options:
```-H, --hdf5  Toggles on write to HDF5 file format```  

## dfoil_hdf5.py  
dfoil_hdf5.py saves dfoil output to the same HDF5 file as above as fasta2dfoil if the -H, --hdf5 option is used. The original script runs if the -H flag is not provided. I removed the precheck redirect in the .sh script so it will print to STDOUT.  

Added options:  
```-H, --hdf5  Toggles on write to HDF5 file format```  

### dfoiler_alt_hdf5.sh  

This runs dfoil.py with GNU parallel.  

## dfoil_analyze_hdf5.py (optional)  

Calculates summary statistics from dfoil_hdf5.py output. Not necessary for downstream scripts.  

Additional options added:  
```-H, --hdf5  Append output to HDF5 file```

### dfoil_analyze_hdf5.sh  

Runs dfoil_analyze_hdf5.py in parallel (with GNU parallel).  

## summarize_alt_hdf5.py  
summarize_alt_hdf5.py replaces the summarizer_alt.sh script from [ExDFOIL](https://github.com/SheaML/ExDFOIL) and writes output to HDF5 tables.  I wrote this one from scratch because the bash script used in ExDFOIL couldn't read from HDF5 files. Also it wasn't working correctly and I couldn't figure out why.  

Required Arguments:  

```-i, --infile  Output from dfoil_hdf5.py```

### runSummary.sh  

This runs the summarize_alt_hdf5.py script with GNU parallel.  

## merge_hdf5.py  
If using [ExDFOIL](https://github.com/SheaML/ExDFOIL) with GNU parallel, this script merges all the individual HDF5 files into a single separate file/table.  

This script merges all the HDF5 summary tables into a single file.  

Required Options:  
```
-p, --path  Specify path to directory containing ONLY HDF5 files  
-o, --out  Specify merged HDF5 filename  
```

## associate.sh  

This is the same as used in ExDFOIL. It associates sample info with each line of the summarized_appended output.  






