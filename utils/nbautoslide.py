#!/usr/bin/env python
# (Re)generate slide metadata automatically
"""
usage:

python nbautoslide.py notebooks...
"""

import io, os, sys, types, re
import argparse
import nbformat


def prefix_code(code, prefix):
    return prefix + code.replace('\n', '\n' + prefix)
    
def print_utf8(s):
    sys.stdout.buffer.write(s.encode('utf-8'))

# Slide types
SLIDE = 'slide'
SUBSLIDE = 'subslide'
FRAGMENT = 'fragment'
SKIP = 'skip'
NO_SLIDE = 'none'

CHARS_PER_LINE = 70   
LINES_PER_SLIDE = 15

def estimate_lines(cell):
    lines = 0
    if cell.cell_type == 'code':
        code = cell.source
        lines = code.count('\n') + 1
        
    if cell.cell_type == 'markdown':
        text = cell.source
        lines = int(len(text) / CHARS_PER_LINE) + text.count('\n') + 1

    if 'outputs' in cell:
        for output in cell.outputs:
            if 'data' in output:
                data = output.data
                if 'text/plain' in data:
                    text_data = data['text/plain']
                    lines += text_data.count('\n') + 1
            elif 'text' in output:
                text_data = output.text
                lines += text_data.count('\n') + 1
            else:
                # Assume the worst
                lines = LINES_PER_SLIDE

        # print(repr(cell.outputs)[:20] + "..." + "\t" + repr(lines))
        
    # print(repr(cell.source[:20] + "...") + "\t" + repr(lines))

    return lines

def autoslide_notebook(notebook_path, args):
    # load the notebook
    if notebook_path == '-':
        notebook = nbformat.read(sys.stdin, 4)
    else:
        with io.open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, 4)

    changed_cells = 0
    prev_cell = None
    lines = 0

    for cell in notebook.cells:
        slide_type = FRAGMENT # Default

        if cell.cell_type == 'markdown':
            if cell.source.startswith('# ') or cell.source.startswith('## '):
                # Main header
                slide_type = SLIDE
            elif cell.source.startswith('#') or cell.source.startswith('**'):
                # Sub header
                slide_type = SUBSLIDE
        
        elif cell.cell_type == 'code':
            if cell.source.startswith('import ') or cell.source.startswith('from '):
                # Generally uninteresting
                slide_type = SKIP

        else:
            # Unknown cell type
            slide_type = SKIP
        
        # Check for overflows
        cell_lines = estimate_lines(cell)
        if slide_type == FRAGMENT:
            if lines + cell_lines > LINES_PER_SLIDE:
                slide_type = SUBSLIDE
                lines = cell_lines
            else:
                lines += cell_lines
        elif slide_type == SLIDE or slide_type == SUBSLIDE:
            lines = cell_lines
            
        # if args.in_place:
        #     print(repr(cell.source[:20] + "...") + "\t" + slide_type + "\t" + repr(lines))

        # Set slide type
        if args.reset or 'metadata' not in cell or 'slideshow' not in cell.metadata:
            if 'metadata' not in cell:
                cell['metadata'] = {}
            if 'slideshow' not in cell.metadata:
                cell.metadata['slideshow'] = {}
            if 'slide_type' not in cell.metadata.slideshow:
                cell.metadata.slideshow['slide_type'] = NO_SLIDE

            old_slide_type = cell.metadata.slideshow.slide_type

            if slide_type != old_slide_type:
                changed_cells += 1
            cell.metadata.slideshow.slide_type = slide_type

        # Save last cell
        last_cell = cell
        

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
    parser.add_argument("--reset", help="reconstruct all slide metadata", action='store_true')
    parser.add_argument("--in-place", help="change notebooks in place", action='store_true')
    parser.add_argument("notebooks", nargs='*', help="notebooks to add slide info to")
    args = parser.parse_args()
    
    for notebook in args.notebooks:
        autoslide_notebook(notebook, args)