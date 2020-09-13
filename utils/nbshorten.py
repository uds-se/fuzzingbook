#!/usr/bin/env python
# Remove excursions from notebooks
"""
usage:

python nbshorten.py notebooks...
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

def link(notebook_path, title):
    notebook_basename = os.path.basename(notebook_path)
    anchor = "#Excursion:-" + title_to_anchor(title)
    return notebook_basename + anchor

RE_NOTEBOOK_TITLE = re.compile(r'#\s\s*(?P<title>[^\n]*).*', re.DOTALL)
RE_BEGIN_EXCURSION = re.compile(r'##*\s\s*Excursion:\s*\s(?P<title>.*)')
RE_END_EXCURSION = re.compile(r'##*\s\s*[eE]nd.*[eE]xcursion')

def shorten_notebook(notebook_path, args):
    # load the notebook
    if notebook_path == '-':
        notebook = nbformat.read(sys.stdin, 4)
    else:
        with io.open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, 4)
            
    in_excursion = False
    changed_cells = 0
    new_cells = []
    notebook_title = None

    for cell in notebook.cells:
        if notebook_title is None:
            match_notebook_title = RE_NOTEBOOK_TITLE.match(cell.source)
            if match_notebook_title:
                notebook_title = match_notebook_title.group('title')
        
        if cell.cell_type == 'markdown':
            match_begin_excursion = RE_BEGIN_EXCURSION.match(cell.source)
            match_end_excursion = RE_END_EXCURSION.match(cell.source)

            if match_begin_excursion:
                in_excursion = True
                changed_cells += 1
                
                if args.links:
                    # Add a link to online version
                    title = match_begin_excursion.group('title')
                    cell.source =  f'(For details on {title}, see ["{notebook_title}" online]({link(notebook_path, title)}).)'
                    new_cells.append(cell)

            elif match_end_excursion:
                in_excursion = False
                changed_cells += 1
        
        if in_excursion:
            # Skip this cell
            changed_cells += 1
        else:
            new_cells.append(cell)
            

    if changed_cells > 0:
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
    parser.add_argument("--links", help="include links to online version", action='store_true')
    parser.add_argument("--in-place", help="change notebooks in place", action='store_true')
    parser.add_argument("notebooks", nargs='*', help="notebooks to add slide info to")
    args = parser.parse_args()
    
    for notebook in args.notebooks:
        shorten_notebook(notebook, args)