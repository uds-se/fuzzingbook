#!/usr/bin/env python
# Update synopsis for given notebook(s)
"""
usage:

python nbsynopsis.py notebook.ipynb
"""

import io, os, sys, types, re

from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

import nbformat
import argparse
import base64
import shutil

SYNOPSIS_TITLE = "## Synopsis"

RXTERM = re.compile('\x1b' + r'\[[^a-zA-Z]*[a-zA-Z]')
def unterm(text):
    """Remove terminal escape commands such as <ESC>[34m"""
    return RXTERM.sub('', text)
    
def convert(svg_filename, png_filename):
    """Convert `svg_filename` into `png_filename`."""

    if os.path.exists('/Applications/Inkscape.app/'):
        # Inkscape on a Mac
        os.system(f"/Applications/Inkscape.app/Contents/MacOS/inkscape -d 300 '{svg_filename}' --export-filename '{png_filename}'")

    elif shutil.which('inkscape'):
        # Inkscape on Linux
        os.system(f"inkscape -d 300 '{svg_filename}' --export-filename '{png_filename}'")

    elif shutil.which('convert'):
        # ImageMagick anywhere
        os.system(f"convert -density 300 '{svg_filename}' '{png_filename}'")

    else:
        raise ValueError("Please install Inkscape (preferred) or ImageMagick")


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
            if cell.cell_type == 'code':
                if cell.source.startswith("# ignore"):
                    pass
                else:
                    synopsis += "```python\n>>> " + cell.source.replace('\n', '\n>>> ') + "\n```\n"
                output_text = ''
                for output in cell.outputs:
                    text = None

                    # SVG output
                    if (text is None and hasattr(output, 'data') and
                        'image/svg+xml' in output.data):
                        svg = output.data['image/svg+xml']
                        if svg is not None:
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
                            
                            convert(svg_filename, png_filename)
                            
                            if 'RENDER_HTML' in os.environ:
                                # Render all HTML and SVG into PNG
                                pics_name = png_basename
                            else:
                                pics_name = svg_basename

                            text = ("```\n" + 
                            '![](' +  'PICS/' + pics_name + ')\n' +
                            '```\n')

                    # PNG output
                    if (text is None and hasattr(output, 'data') and
                        'image/png' in output.data):
                        png = output.data['image/png']
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
                            text = "```\n![](" + 'PICS/' + png_basename + ')\n```\n'

                    # HTML output
                    if (text is None and hasattr(output, 'data') and
                        'text/html' in output.data):
                        text = "```\n" + output.data['text/html'] + "\n```\n"

                    # Markdown output
                    if (text is None and hasattr(output, 'data') and
                       'text/markdown' in output.data):
                        text = "```\n" + output.data['text/markdown'] + "\n```\n"

                    # Text output
                    if text is None and hasattr(output, 'text'):
                        text = unterm(output.text) + "\n"

                    # Data output
                    if (text is None and hasattr(output, 'data') and
                        'text/plain' in output.data):
                        text = unterm(output.data['text/plain'] + '\n')

                    if text is not None:
                        output_text += text

                if output_text:
                    if output_text.startswith('![]'):
                        synopsis += '\n' + output_text + '\n'
                    else:
                        synopsis += "```python\n" + output_text + "```\n"
            else:
                synopsis += cell.source + "\n\n"
    
    synopsis = synopsis.replace("```python\n```\n", "")
    synopsis = synopsis.replace("```\n```python\n", "")
    synopsis = synopsis.replace("```\n```\n", "")

    return synopsis
    
def skip_cell(cell):
    # Don't include in slides
    if 'metadata' not in cell:
        cell['metadata'] = {}
    if 'slideshow' not in cell.metadata:
        cell.metadata['slideshow'] = {}
    if 'slide_type' not in cell.metadata.slideshow:
        cell.metadata.slideshow['slide_type'] = 'skip'
    return cell
    
def update_synopsis(notebook_name, synopsis):
    notebook_path = notebook_name

    # Read notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)
    
    for i, cell in enumerate(notebook.cells):
        if cell.source.startswith("## Synopsis"):
            # Update cell
            if cell.source == synopsis:
                return
            cell.source = synopsis
            cell = skip_cell(cell)
            break
        elif cell.source.startswith("## "):
            # Insert cell before
            new_cell = nbformat.v4.new_markdown_cell(source=synopsis)
            new_cell = skip_cell(new_cell)
            notebook.cells = (notebook.cells[:i] + 
                                [new_cell] + notebook.cells[i:])
            break
            
    # print(nbformat.writes(notebook))
    
    # Write notebook out again
    with io.open(notebook_path, 'w', encoding='utf-8') as f:
        f.write(nbformat.writes(notebook))
        
    print("Updated " + notebook_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", help="project name", default="fuzzingbook")
    parser.add_argument("--update", action='store_true', 
                        help="Update synopsis section")
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
