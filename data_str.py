#!/usr/bin/env python

import tables

class Files(tables.IsDescription):
    header            = tables.StringCol(100)   # 100-character String
    data              = tables.StringCol(300)   # 300-character String
    DFOILheader       = tables.StringCol(420)   # 420-character String
    DFOILdata         = tables.StringCol(600)   # 600-charcter String
    analyzed          = tables.StringCol(150)   # 150-character String
    summary           = tables.StringCol(300)   # 300-character String
