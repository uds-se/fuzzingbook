#!/usr/bin/env python
# Add proper metadata to fuzzingbook notebook

"""
usage:

python add-metadata.py [--project PROJECT] [--titlepage] A.ipynb > A'.ipynb
"""

import io
import os
import sys
import re

import nbformat

def get_text_contents(notebook):
    contents = ""
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            contents += "".join(cell.source) + "\n\n"
            
    # print("Contents of", notebook, ": ", repr(contents[:100]))

    return contents
    

def get_title(notebook):
    """Return the title from a notebook file"""
    contents = get_text_contents(notebook)
    match = re.search(r'^# (.*)', contents, re.MULTILINE)
    title = match.group(1).replace(r'\n', '')
    # print("Title", title.encode('utf-8'))
    return title



def add_document_metadata(notebook, project, titlepage):
    """Add document metadata"""
    # No cell toolbar for published notebooks
    if 'celltoolbar' in notebook.metadata:
        del notebook.metadata['celltoolbar']

    # Add bibliography
    if 'ipub' not in notebook.metadata:
        notebook.metadata['ipub'] = {}
    if 'bibliography' not in notebook.metadata['ipub']:
        notebook.metadata['ipub']['bibliography'] = 'fuzzingbook.bib'

    if titlepage:
        # Add title
        chapter_title = get_title(notebook)
        if project == 'fuzzingbook':
            notebook.metadata['ipub']['titlepage'] = {
                "author": "Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler",
                "title": chapter_title,
                "subtitle": 'A Chapter of "The Fuzzing Book"'
            }
        elif project == 'debuggingbook':
            notebook.metadata['ipub']['titlepage'] = {
                "author": "Andreas Zeller",
                "title": chapter_title,
                "subtitle": 'A Chapter of "The Debugging Book"'
            }

    # Add table of contents
    notebook.metadata['toc'] = {
     "base_numbering": 1,
     "nav_menu": {},
     "number_sections": True,
     "sideBar": True,
     "skip_h1_title": True,
     "title_cell": "",
     "title_sidebar": "Contents",
     "toc_cell": False,
     "toc_position": {},
     "toc_section_display": True,
     "toc_window_display": True
    }
    notebook.metadata["toc-autonumbering"] = False

def add_solution_metadata(notebook):
    """Add solution metadata"""
    
    within_solution = False
    previous_cell = None
    
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            text = cell.source
            if text.startswith("**Solution"):
                within_solution = True
                previous_cell.metadata['solution2_first'] = True
                previous_cell.metadata['solution2'] = 'hidden'
            elif text.startswith("#"):
                within_solution = False

        if within_solution:
            cell.metadata['solution2'] = 'hidden'
            if 'slideshow' not in cell.metadata:
                cell.metadata['slideshow'] = {}
                cell.metadata['slideshow']['slide_type'] = "skip"

        previous_cell = cell
                


def add_metadata(filename, project, titlepage):
    # Read in
    with io.open(filename, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    add_document_metadata(notebook, project, titlepage)
    add_solution_metadata(notebook)

    # Write out
    # Include a newline at the end, as Jupyterlab does
    notebook_content = nbformat.writes(notebook) + '\n'
    sys.stdout.buffer.write(notebook_content.encode('utf-8'))
    

    
if __name__ == '__main__':
    args = sys.argv[1:]
    
    if args[0] == "--project":
        project = args[1]
        args = args[2:]
    else:
        project = 'fuzzingbook'

    if args[0] == "--titlepage":
        titlepage = True
        args = args[1:]
    else:
        titlepage = False
        
    notebooks = args

    if not notebooks:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    
    for notebook in notebooks:
        add_metadata(notebook, project, titlepage)
