#!/usr/bin/env python
# Apply autopep8 on code cells of given notebook
"""
usage:

python nbautopep8.py [autopep8 options] notebooks...
"""

import io, os, sys, types, re

import nbformat
import autopep8

# If True, split cells that contain more than one def/use
split_cells = False

def prefix_code(code, prefix):
    return prefix + code.replace('\n', '\n' + prefix)
    
def print_utf8(s):
    sys.stdout.buffer.write(s.encode('utf-8'))

def autopep8_notebook(job_args):
    notebook_path, options = job_args

    # load the notebook
    if notebook_path == '-':
        notebook = nbformat.read(sys.stdin, 4)
    else:
        with io.open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, 4)

    changed_cells = 0
    i = 0
    
    while i < len(notebook.cells):
        cell = notebook.cells[i]

        if cell.cell_type != 'code':
            i += 1
            continue
            
        if cell.source.startswith('!'):
            # Shell magic -- leave unchanged
            i += 1
            continue

        code = cell.source + '\n'
        
        # run autopep8 on it
        fixed_code = autopep8.fix_code(code, options)

        code_sep = fixed_code.find('\n\n\n')
        if split_cells and code_sep >= 0:
            # Multiple defs/uses in one cell; split
            this_code = fixed_code[:code_sep + 1].strip()
            next_code = fixed_code[code_sep + 3:].strip()
            
            if len(this_code) > 0 and len(next_code) > 0:
                next_cell = nbformat.v4.new_code_cell(next_code)
                if cell.metadata:
                    next_cell.metadata = cell.metadata
                cell.source = this_code
                notebook.cells = notebook.cells[:i] + [cell] + [next_cell] + notebook.cells[i + 1:]
                changed_cells += 1
                continue

        if code.strip() == fixed_code.strip():
            i += 1
            continue

        # Set it again
        cell.source = fixed_code.strip()
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
    args = sys.argv[1:]
    if len(args) == 0 or args[0] == "--help" or args[0] == "-h":
        print("usage: nbautopep8 [--split-cells] [autopep8-options...] notebooks...")
        print("Automatically formats Python code cells in notebooks")
        print("to conform to the PEP 8 style guide.")
        print()
        print("autopep8-options include:")

    if len(args) > 0 and (args[0] == "--split-cells" or args[0] == "-s"):
        split_cells = True
        args = args[1:]
    
    args = autopep8.parse_args(args, apply_config=True)
    
    if args.diff:
        print("Unsupported option: --diff")
        sys.exit(2)
    if args.recursive:
        print("Unsupported option: --recursive")
        sys.exit(2)
    if args.line_range:
        print("Unsupported option: --line-range")
        sys.exit(2)

    if args.jobs > 1:
        import multiprocessing
        pool = multiprocessing.Pool(args.jobs)
        pool.map(autopep8_notebook,
                 [(notebook, args) for notebook in args.files])
    else:
        for notebook in args.files:
            autopep8_notebook((notebook, args))
