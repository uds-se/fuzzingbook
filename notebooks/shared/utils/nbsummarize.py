#!/usr/bin/env python
# Update synopsis and summaries for given notebook(s)
"""
usage:

python nbsummarize.py notebook.ipynb
"""

import io, os, sys, types, re

from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

import nbformat
import argparse
import base64

SYNOPSIS_TITLE = "## Synopsis"
SUMMARY_TITLE = "### Summary"

img_count = 1

def cell_to_text(cell, notebook_path, notebook_basename):
    """Convert a cell (and its output) into a single Markdown text."""
    if cell.cell_type != 'code':
        return cell.source + "\n\n"
    
    # Code cell
    synopsis = "```python\n>>> " + cell.source.replace('\n', '\n>>> ') + "\n```\n"
    output_text = ''
    
    for output in cell.outputs:
        text = None

        # SVG output
        if text is None:
            svg = None
            try:
                svg = output.data['image/svg+xml']
            except KeyError:
                pass
            except AttributeError:
                pass
            if svg is not None:
                global img_count
                
                svg_basename = (notebook_basename +
                    '-synopsis-' + repr(img_count) + '.svg')
                png_basename = (notebook_basename +
                    '-synopsis-' + repr(img_count) + '.png')
                img_count += 1
                
                svg_filename = os.path.join(
                    os.path.dirname(notebook_path),
                    'PICS', svg_basename)
                png_filename = os.path.join(
                    os.path.dirname(notebook_path),
                    'PICS', png_basename)
                    
                print("Creating", svg_filename)
                with open(svg_filename, "w") as f:
                    f.write(svg)
                    
                print("Creating", png_filename)
                os.system('convert -density 300 ' + svg_filename + ' ' + png_filename)
                
                if 'RENDER_HTML' in os.environ:
                    # Render all HTML and SVG into PNG
                    text = "![](" + 'PICS/' + png_basename + ')'
                else:
                    text = "![](" + 'PICS/' + svg_basename + ')'

        # PNG output
        if text is None:
            png = None
            try:
                png = output.data['image/png']
            except KeyError:
                pass
            except AttributeError:
                pass
            if png is not None:
                png_basename = (notebook_basename +
                    '-synopsis-' + repr(img_count) + '.png')
                img_count += 1
                                                
                png_filename = os.path.join(
                    os.path.dirname(notebook_path),
                    'PICS', png_basename)
                    
                print("Creating", png_filename)
                with open(png_filename, "wb") as f:
                    f.write(base64.b64decode(png, validate=True))
                text = "![](" + 'PICS/' + png_basename + ')'

        # Text output
        if text is None:
            try:
                text = output.text
            except AttributeError:
                pass

        # Data output
        if text is None:
            try:
                text = output.data['text/plain']
            except KeyError:
                pass
        
        if text is not None:
            output_text += text + '\n'

    if output_text:
        if output_text.startswith('![]'):
            synopsis += '\n' + output_text + '\n'
        else:
            synopsis += "```python\n" + output_text + "```\n"
            
    return synopsis


def notebook_synopsis(notebook_name):
    notebook_path = notebook_name

    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)
        
    synopsis = ""
    in_synopsis = False
    first_synopsis = True
    img_count = 1
    
    notebook_noext = os.path.splitext(notebook_path)[0]
    notebook_basename = os.path.basename(notebook_noext)
    
    for cell in notebook.cells:
        if not first_synopsis and cell.source.startswith(SYNOPSIS_TITLE):
            in_synopsis = True
            synopsis = SYNOPSIS_TITLE + f"""
<!-- Automatically generated. Do not edit. -->

To [use the code provided in this chapter](Importing.ipynb), write

```python
>>> from {args.project}.{notebook_basename} import <identifier>
```

and then make use of the following features.
"""
            synopsis += cell.source[len(SYNOPSIS_TITLE):] + "\n\n"
            continue
        elif cell.source.startswith("## "):
            in_synopsis = False
            first_synopsis = False

        if in_synopsis:
            synopsis += cell_to_text(cell, notebook_path, notebook_basename)
    
    synopsis = synopsis.replace("```\n```python\n", "")

    return synopsis


def update_synopsis(notebook_name, synopsis):
    notebook_path = notebook_name
    global img_count
    img_count = 1

    # Read notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)
    
    for i, cell in enumerate(notebook.cells):
        if cell.source.startswith("## Synopsis"):
            # Update cell
            if cell.source == synopsis:
                return
            cell.source = synopsis
            break
        elif cell.source.startswith("## "):
            # Insert cell before
            new_cell = nbformat.v4.new_markdown_cell(source=synopsis)
            notebook.cells = (notebook.cells[:i] + 
                                [new_cell] + notebook.cells[i:])
            break
            
    # print(nbformat.writes(notebook))
    
    # Write notebook out again
    with io.open(notebook_path, 'w', encoding='utf-8') as f:
        f.write(nbformat.writes(notebook))
        
    print("Updated " + notebook_path)


# TODO: Have the "summarize" function return a target spec (section titles) for each summary
# The summary would then be inserted at the beginning of each section

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", help="project name", default="fuzzingbook")
    parser.add_argument("--update", action='store_true', 
                        help="Update summaries")
    parser.add_argument("notebooks", nargs='*', help="notebooks to extract/update synopsis for")
    args = parser.parse_args()

    for notebook in args.notebooks:
        synopsis = notebook_synopsis(notebook)
        if not synopsis:
            continue

        if args.update:
            update_synopsis(notebook, synopsis)
        else:
            print(synopsis, end='') 
