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
    i = 0
    
    while i < len(notebook.cells):
        cell = notebook.cells[i]

        if cell.cell_type != 'code':
            i += 1
            continue
            
        # magic in the cell (say "%matplotlib inline") remains as is
        code = cell.source + '\n'
        
        # run autopep8 on it
        fixed_code = autopep8.fix_code(code, options)

        code_sep = fixed_code.find('\n\n\n')
        if code_sep >= 0:
            # Multiple defs/uses in one cell; split
            this_code = fixed_code[:code_sep + 1].strip()
            next_code = fixed_code[code_sep + 3:].strip()
            
            if len(this_code) > 0 and len(next_code) > 0:
                # if args.in_place:
                #     print_utf8(notebook_path + ": splitting cell\n")
                #     print_utf8(fixed_code + "\n")
                #     print_utf8("into\n")
                #     print_utf8(this_code + "\n")
                #     print_utf8("---\n")
                #     print_utf8(next_code + "\n")
                
                next_cell = nbformat.v4.new_code_cell(next_code)
                if cell.metadata:
                    next_cell.metadata = cell.metadata
                cell.source = this_code
                notebook.cells = notebook.cells[:i] + [cell] + [next_cell] + notebook.cells[i + 1:]
                changed_cells += 1
                continue

        # Avoid having whitespace at the beginning or end of code cells
        # fixed_code = fixed_code.strip()
        if code == fixed_code:
            i += 1
            continue

        # Set it again
        cell.source = fixed_code
        changed_cells += 1
        i += 1

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
