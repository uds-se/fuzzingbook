#!/usr/bin/env python

import io, os, sys, types, re
import datetime

# from IPython import get_ipython
# from IPython.core.interactiveshell import InteractiveShell

import nbformat
from import_notebooks import RE_CODE

# Things to ignore in exported Python code
RE_IGNORE = re.compile(r'^import fuzzingbook_utils$|^get_ipython().*|^%.*')

# Strip blank lines
RE_BLANK_LINES = re.compile(r'^[ \t]*$', re.MULTILINE)

# Comments
RE_COMMENTS = re.compile(r'^#.*$', re.MULTILINE)

# Common header for all code
HEADER = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/{module}.html
# Last change: {timestamp}
#
# This material is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International License
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)

"""

def is_all_comments(code):
    executable_code = re.sub(RE_COMMENTS, '', code).strip()
    return executable_code == ""

def prefix_code(code, prefix):
    return prefix + code.replace('\n', '\n' + prefix)
    
def indent_code(code):
    lines = prefix_code(code, "    ")
    return re.sub(RE_BLANK_LINES, '', lines)

def first_line(text):
    index = text.find('\n')
    if index >= 0:
        return text[:index]
    else:
        return text

def print_utf8(s):
    sys.stdout.buffer.write(s.encode('utf-8'))

def print_if_main(code):
    # Run code only if run as main file
    print_utf8('\nif __name__ == "__main__":\n')
    print_utf8(indent_code(code) + "\n\n")

def export_notebook_code(notebook_name, path=None):
    # notebook_path = import_notebooks.find_notebook(notebook_name, path)
    notebook_path = notebook_name

    # load the notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)

    # shell = InteractiveShell.instance()

    # Get versioning info
    notebook_modification_time = os.path.getmtime(notebook_path)    
    timestamp = datetime.datetime.fromtimestamp(notebook_modification_time) \
        .astimezone().isoformat(sep=' ', timespec='seconds')
    module = os.path.splitext(os.path.basename(notebook_name))[0]

    header = HEADER.format(module=module, timestamp=timestamp)
    print_utf8(header)
    sep = ''

    for cell in notebook.cells:
        if cell.cell_type == 'code':
            code = cell.source
            if len(code.strip()) == 0:
                # Empty code
                continue
            
            bang = False
            if code.startswith('!'):
                code = "import os\nos.system(r" + repr(code[1:]) + ")"
                bang = True

            if RE_IGNORE.match(code):
                # Code to ignore - comment out
                print_utf8("\n" + prefix_code(code, "# ") + "\n")
            elif RE_CODE.match(code) and not bang:
                # Export the code as is
                print_utf8("\n" + code + "\n")
            elif is_all_comments(code):
                # Only comments
                print_utf8("\n" + code + "\n")
            else:
                print_if_main(code)
        else:
            # Anything else
            contents = cell.source
            print_utf8("\n" + prefix_code(contents, "# ") + "\n")
            if contents.startswith('#'):
                # Header
                print_if_main("print(" + repr(sep + first_line(contents)) + ")\n\n")
                sep = '\n'

if __name__ == "__main__":
    for notebook in sys.argv[1:]:
        export_notebook_code(notebook)
