#!/bin/bash

mkdir -p summary
file=counts/cuatrocienegas_UOG2018p1.cyanostictus1_JJW564p1.oberonS3_SML150.oberon3_JJW605p1.tab.h5
fileraw=`basename $file`
echo $(echo "$fileraw" | cut -d'.' -f1-4 --output-delimiter=' ')
