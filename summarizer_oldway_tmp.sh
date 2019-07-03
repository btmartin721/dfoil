#!/bin/bash
mkdir -p summary
read file
fileraw=`basename "$file"`
echo $(tail -n 1 "$file" | cut -f4,5,7,11 | awk  '{print($4," ",$3," ",$2," ",$1)}')
