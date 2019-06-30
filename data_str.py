#!/usr/bin/env python

import tables

class Files(tables.IsDescription):
    header            = tables.StringCol(300)   # 300-character String
    data              = tables.StringCol(300)   # 300-character String
