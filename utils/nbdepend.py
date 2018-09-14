#!/usr/bin/env python
# Issue dependencies for given notebook(s)
"""
usage:

python nbdepend.py A.ipynb B.ipynb C.ipynb > Makefile_deps
"""

import io, os, sys, types, re

from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

import nbformat

RE_IMPORT = re.compile(r"^ *import  *([a-zA-Z0-9_]+)", re.MULTILINE)
RE_FROM = re.compile(r"^ *from  *([a-zA-Z0-9_]+)  *import", re.MULTILINE)

def print_notebook_dependencies(notebook_name, path=None):
    # notebook_path = import_notebooks.find_notebook(notebook_name, path)
    notebook_path = notebook_name

    # load the notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)

    shell = InteractiveShell.instance()

    modules = set()
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            # transform the input to executable Python
            code = shell.input_transformer_manager.transform_cell(cell.source)
            for match in re.finditer(RE_IMPORT, code):
                modules.add(match.group(1))
            for match in re.finditer(RE_FROM, code):
                modules.add(match.group(1))
                
    for module in modules:
        print(module)


if __name__ == "__main__":
    for notebook in sys.argv[1:]:
        print_notebook_dependencies(notebook)
