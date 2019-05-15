#!/usr/bin/env python
# Update synopsis for given notebook(s)
"""
usage:

python nbsynopsis.py notebook.ipynb
"""

import io, os, sys, types, re

from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

import nbformat
import argparse

SYNOPSIS_TITLE = "## Synopsis"

def notebook_synopsis(notebook_name):
    notebook_path = notebook_name

    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)
        
    synopsis = ""
    in_synopsis = False
    first_synopsis = True
    
    for cell in notebook.cells:
        if not first_synopsis and cell.source.startswith(SYNOPSIS_TITLE):
            in_synopsis = True
            synopsis = SYNOPSIS_TITLE + "\n\n<!-- Automatically generated. Do not edit. -->\n\n"
            continue
        elif cell.source.startswith("## "):
            in_synopsis = False
            first_synopsis = False

        if in_synopsis:
            if cell.cell_type == 'code':
                synopsis += "```python\n" + cell.source + "\n```\n"
                for output in cell.outputs:
                    synopsis += "```\n=> " + output.text + "```\n"
            else:
                synopsis += cell.source + "\n\n"
            
    return synopsis
    
def update_synopsis(notebook_name, synopsis):
    notebook_path = notebook_name

    # Read notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)
    
    for i, cell in enumerate(notebook.cells):
        if cell.source.startswith("## Synopsis"):
            # Update cell
            if cell.source == synopsis:
                return
            cell.source = synopsis
            break
        elif cell.source.startswith("## "):
            # Insert cell before
            new_cell = nbformat.v4.new_markdown_cell(source=synopsis)
            notebook.cells = (notebook.cells[:i] + 
                                [new_cell] + notebook.cells[i:])
            break
            
    # print(nbformat.writes(notebook))
    
    # Write notebook out again
    with io.open(notebook_path, 'w', encoding='utf-8') as f:
        f.write(nbformat.writes(notebook))
        
    print("Updated " + notebook_path)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action='store_true', help="Produce graph")
    parser.add_argument("notebooks", nargs='*', help="notebooks to extract/update synopsis for")
    args = parser.parse_args()

    for notebook in args.notebooks:
        synopsis = notebook_synopsis(notebook)
        if args.update:
            update_synopsis(notebook, synopsis)
        else:
            print(synopsis, end='')        
