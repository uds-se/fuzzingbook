#!/usr/bin/env python
# Create table of contents for given notebook(s)
"""
usage:

python nbtoc.py A.ipynb B.ipynb C.ipynb
"""

import io, os, sys, types, re

import nbformat
import argparse


def get_text_contents(notebook):
    with io.open(notebook, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    contents = ""
    for cell in nb.cells:
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

def notebook_toc_entry(notebook_name, prefix, path=None):
    # notebook_path = import_notebooks.find_notebook(notebook_name, path)
    notebook_path = notebook_name
    notebook_title = get_title(notebook_path)
    notebook_base = os.path.basename(notebook_path)

    return prefix + " [" + notebook_title + "](" + notebook_base + ")\n"
    
def notebook_toc(public_chapters, appendices):
    title = "# Generating Software Tests"

    chapter_toc = "## Table of Contents\n\n"
    counter = 1
    for notebook in public_chapters:
        notebook_title = get_title(notebook)
        if notebook_title.startswith("Part "):
            # chapter_toc += "\n### " + notebook_title + "\n\n"
            chapter_toc += "\n" + notebook_toc_entry(notebook, "###") + "\n"
        else:
            chapter_toc += notebook_toc_entry(notebook, "*") # repr(counter) + ".")
            counter += 1

    appendix_toc = "## Appendices\n\n"
    for notebook in appendices:
        appendix_toc += notebook_toc_entry(notebook, "*")

    toc_notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell(source=title),
            nbformat.v4.new_markdown_cell(source=chapter_toc),
            nbformat.v4.new_markdown_cell(source=appendix_toc)
        ])

    # Get along with TOC extension
    toc_notebook.metadata['toc'] = {
     "base_numbering": 1,
     "nav_menu": {},
     "number_sections": False,
     "sideBar": False,
     "skip_h1_title": False,
     "title_cell": "",
     "title_sidebar": "Contents",
     "toc_cell": False,
     "toc_position": {},
     "toc_section_display": False,
     "toc_window_display": False
    }
    
    # Add general metadata
    toc_notebook.metadata["kernelspec"] = {
     "display_name": "Python 3",
     "language": "python",
     "name": "python3"
    }
    
    toc_notebook.metadata["language_info"] = {
     "codemirror_mode": {
      "name": "ipython",
      "version": 3
     },
     "file_extension": ".py",
     "mimetype": "text/x-python",
     "name": "python",
     "nbconvert_exporter": "python",
     "pygments_lexer": "ipython3",
     "version": "3.6.6"
    }

    return toc_notebook    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapters", help="List of public chapters")
    parser.add_argument("--appendices", help="List of appendices")
    args = parser.parse_args()

    public_chapters = args.chapters.split()
    appendices = args.appendices.split()
    
    toc_notebook = notebook_toc(public_chapters, appendices)
    sys.stdout.buffer.write(nbformat.writes(toc_notebook).encode("utf-8"))
