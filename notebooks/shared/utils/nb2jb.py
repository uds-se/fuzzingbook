#!/usr/bin/env python
# Set up notebooks for Jupyter Books:
# * hide `#ignore` cells
#
# All changes are made by adding metadata; in Jupyter, the file stays unchanged.
"""
usage:

python nb2jb.py notebooks...
"""

import io, os, sys, types, re
import argparse
import nbformat

def prefix_code(code, prefix):
    return prefix + code.replace('\n', '\n' + prefix)
    
def print_utf8(s):
    sys.stdout.buffer.write(s.encode('utf-8'))
    
def title_to_anchor(title):
    return title.replace(' ', '-').replace('`', '')

def link(site_prefix, notebook_path, title):
    notebook_basename = os.path.splitext(os.path.basename(notebook_path))[0]
    anchor = "#Excursion:-" + title_to_anchor(title)
    return site_prefix + notebook_basename + ".html" + anchor
    
RE_IGNORE = r'(quiz|display|#\signore)'
re_ignore = re.compile(RE_IGNORE)

def setup_notebook(notebook_path, args):
    # load the notebook
    if notebook_path == '-':
        notebook = nbformat.read(sys.stdin, 4)
    else:
        with io.open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, 4)
            
    changed_cells = 0
    new_cells = []
    remove_tag = "remove-input"

    for cell in notebook.cells:
        if cell.cell_type == 'code':
            source = cell.source.strip()
            if re_ignore.match(source):
                cell_tags = cell.get('metadata', {}).get('tags', [])
                if remove_tag not in cell_tags:
                    cell_tags.append(remove_tag)
                    cell['metadata']['tags'] = cell_tags
                    changed_cells += 1
        new_cells.append(cell)

    notebook.cells = new_cells
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-place", help="change notebooks in place", action='store_true')
    parser.add_argument("notebooks", nargs='*', help="notebooks to add slide info to")
    args = parser.parse_args()
    
    for notebook in args.notebooks:
        setup_notebook(notebook, args)