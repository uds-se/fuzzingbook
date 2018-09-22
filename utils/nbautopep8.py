#!/usr/bin/env python
# Apply autopep8 on code cells of given notebook
"""
usage:

python nbautopep8.py [autopep8 options] notebooks...
"""

import io, os, sys, types, re

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

    changed_cells = 0
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            # magic in the cell (say "%matplotlib inline") remains as is
            code = cell.source + '\n'
            
            # run autopep8 on it
            fixed_code = autopep8.fix_code(code, options)
            
            if args.in_place and fixed_code.find('\n\n\n') >= 0:
                print(notebook_path + ": warning: definition and use in one cell; consider split:")
                print(fixed_code)

            # Avoid having whitespace at the beginning or end of code cells
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
    
    if args.diff:
        print("Unsupported option: --diff")
        sys.exit(2)
    if args.recursive:
        print("Unsupported option: --recursive")
        sys.exit(2)
    if args.line_range:
        print("Unsupported option: --line-range")
        sys.exit(2)
    if args.jobs != 1:
        print("Unsupported option: --jobs")
        sys.exit(2)

    for notebook in args.files:
        autopep8_notebook(notebook, args)
