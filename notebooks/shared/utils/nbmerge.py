#!/usr/bin/env python
# Note, updated version of 
# https://github.com/ipython/ipython-in-depth/blob/master/tools/nbmerge.py
"""
usage:

python nbmerge.py A.ipynb B.ipynb C.ipynb > merged.ipynb
"""

import io
import os
import sys

import nbformat

def merge_notebooks(filenames):
    merged = None
    for fname in filenames:
        with io.open(fname, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        if merged is None:
            merged = nb
        else:
            # TODO: add an optional marker between joined notebooks
            # like an horizontal rule, for example, or some other arbitrary
            # (user specified) markdown cell)
            merged.cells.extend(nb.cells)
    if not hasattr(merged.metadata, 'name'):
        merged.metadata.name = ''
    merged.metadata.name += "_merged"
    sys.stdout.buffer.write(nbformat.writes(merged).encode('utf-8'))

if __name__ == '__main__':
    notebooks = sys.argv[1:]
    if not notebooks:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
        
    merge_notebooks(notebooks)