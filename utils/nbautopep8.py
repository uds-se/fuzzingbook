#!/usr/bin/env python
# Apply autopep8 on code cells of given notebook
"""
usage:

python nbautopep8.py [autopep8 options] notebooks...
"""

import io, os, sys, types, re

from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

import nbformat
import autopep8

def prefix_code(code, prefix):
    return prefix + code.replace('\n', '\n' + prefix)
    
def print_utf8(s):
    sys.stdout.buffer.write(s.encode('utf-8'))

def autopep8_notebook(notebook_path, options={}):
    # load the notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)

    shell = InteractiveShell.instance()

    changed_cells = 0
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            # transform the input to executable Python
            code = shell.input_transformer_manager.transform_cell(cell.source)
            
            # run autopep8 on it
            fixed_code = autopep8.fix_code(code, options)
            
            # We generally have no whitespace at the beginning or end of cells
            # fixed_code = fixed_code.strip()

            if code == fixed_code:
                continue

            # Set it again
            cell.source = fixed_code
            changed_cells += 1

    notebook_contents = (nbformat.writes(notebook) + '\n').encode('utf-8')

    if args.in_place:
        if changed_cells > 0:
            temp_notebook_path = notebook_path + "~"
            with io.open(temp_notebook_path, 'wb') as f:
                f.write(notebook_contents)
            os.rename(temp_notebook_path, notebook_path)
            print("%s: %d cell(s) changed" % (notebook_path, changed_cells))
        else:
            print("%s: unchanged" % notebook_path)
    else:
        sys.stdout.buffer.write(notebook_contents)

if __name__ == "__main__":
    args = autopep8.parse_args(sys.argv[1:], apply_config=True)
    
    if args.diff or args.recursive or args.ignore or args.line_range or args.jobs:
        print("Unsupported option")
        sys.exit(2)

    for notebook in args.files:
        autopep8_notebook(notebook, args)
