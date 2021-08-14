#!/usr/bin/env python
# Print statistics for given notebook(s)
"""
usage:

python nbstats.py A.ipynb B.ipynb C.ipynb
"""

import io, os, sys, types, re

import nbformat

def notebook_stats(notebook_name, path=None):
    # notebook_path = import_notebooks.find_notebook(notebook_name, path)
    notebook_path = notebook_name

    # load the notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)
        
    notebook_loc = 0
    notebook_words = 0

    for cell in notebook.cells:
        if cell.cell_type == 'code':
            cell_loc = cell.source.replace('\n\n', '\n').strip().count('\n') + 1
            # print(cell.source.encode('utf8'), cell_loc)
            notebook_loc += cell_loc
        else:
            cell_words = len(cell.source.split())
            # print(cell.source.encode('utf8'), cell_words)
            notebook_words += cell_words
    
    return notebook_loc, notebook_words

FORMAT = "%35s%6d LOC%7d words"

if __name__ == "__main__":
    total_loc = 0
    total_words = 0
    for notebook in sys.argv[1:]:
        notebook_loc, notebook_words = notebook_stats(notebook)
        print(FORMAT % (notebook, notebook_loc, notebook_words))
        total_loc += notebook_loc
        total_words += notebook_words
        
    if len(sys.argv) > 2:
        print(FORMAT % ("Total", total_loc, total_words))
        