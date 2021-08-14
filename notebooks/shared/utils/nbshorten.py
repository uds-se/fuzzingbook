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

def link(site_prefix, notebook_path, title):
    notebook_basename = os.path.splitext(os.path.basename(notebook_path))[0]
    anchor = "#Excursion:-" + title_to_anchor(title)
    return site_prefix + notebook_basename + ".html" + anchor

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
    skipped_cells = 0
    new_cells = []
    notebook_title = None

    for cell in notebook.cells:
        skip_this_cell = in_excursion

        if notebook_title is None:
            match_notebook_title = RE_NOTEBOOK_TITLE.match(cell.source)
            if match_notebook_title:
                notebook_title = match_notebook_title.group('title')
        
        if cell.cell_type == 'markdown':
            match_begin_excursion = RE_BEGIN_EXCURSION.match(cell.source)
            match_end_excursion = RE_END_EXCURSION.match(cell.source)

            if match_begin_excursion:
                skip_this_cell = True
                in_excursion = True
                
                if args.link_to:
                    # Add a link to online version
                    title = match_begin_excursion.group('title')
                    cell.source =  f'({title} can be found in ["{notebook_title}" online]({link(args.link_to, notebook_path, title)}).)'
                    skip_this_cell = False

            elif match_end_excursion:
                skip_this_cell = True
                in_excursion = False

        if skip_this_cell:
            skipped_cells += 1
            
            if args.skip_slides:
                # Don't include in slides
                if 'metadata' not in cell:
                    cell['metadata'] = {}
                if 'slideshow' not in cell.metadata:
                    cell.metadata['slideshow'] = {}
                if 'slide_type' not in cell.metadata.slideshow:
                    cell.metadata.slideshow['slide_type'] = 'skip'
            
        else:
            new_cells.append(cell)

    notebook.cells = new_cells
    notebook_contents = (nbformat.writes(notebook) + '\n').encode('utf-8')

    if args.in_place:
        if skipped_cells > 0:
            temp_notebook_path = notebook_path + "~"
            with io.open(temp_notebook_path, 'wb') as f:
                f.write(notebook_contents)
            os.rename(temp_notebook_path, notebook_path)
            print("%s: %d cell(s) skipped" % (notebook_path, skipped_cells))
        else:
            print("%s: unchanged" % notebook_path)
    else:
        sys.stdout.buffer.write(notebook_contents)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--link-to", help="link to online version on given site")
    parser.add_argument("--skip-slides", help="skip excursion cells in slides", action='store_true')
    parser.add_argument("--in-place", help="change notebooks in place", action='store_true')
    parser.add_argument("notebooks", nargs='*', help="notebooks to add slide info to")
    args = parser.parse_args()
    
    for notebook in args.notebooks:
        shorten_notebook(notebook, args)