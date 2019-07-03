#1/bin/bash

parallel './summarizer_alt_hdf5.py -i $(echo {})' ::: counts/*.tab.h5
