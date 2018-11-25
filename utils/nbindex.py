#!/usr/bin/env python
# Produce index for given notebook(s)
"""
usage:

python nbindex.py A.ipynb B.ipynb C.ipynb
"""

import io, os, sys, types, re
import nbformat
import string


def format_code(s):
    return "`" + s + "`"

def format_function(s):
    return format_code(s + "()")

def format_class(s):
    return format_code(s) + " class"

def format_text(s):
    return s

def title_to_fragment(s):
    return "#" + s.replace(" ", "-")

ITEMS = {
    'code': [
        ("function", re.compile(r"^def +([A-Za-z0-9_]+)", re.MULTILINE), format_function),
        ("class",    re.compile(r"^class +([A-Za-z0-9_]+)", re.MULTILINE), format_class),
        ("method",   re.compile(r"^ +def +([A-Za-z0-9_]+)", re.MULTILINE), format_function),
        ("constant", re.compile(r"^ *([A-Z][A-Z0-9_]+) += ", re.MULTILINE), format_code)
    ],
    'markdown': [
        ("def_1", re.compile(r"[^_]_([a-zA-Z]+)_[^_]"), format_text),
        ("def_2", re.compile(r"[^_]_([a-zA-Z]+ [a-zA-Z]+)_[^_]"), format_text),
        ("def*1", re.compile(r"[^*]\*([a-zA-Z]+)\*[^*]"), format_text),
        ("def*2", re.compile(r"[^*]\*([a-zA-Z]+ [a-zA-Z]+)\*[^*]"), format_text),
        ("ref`function", re.compile(r"`([a-zA-Z0-9_]+)\(`"), format_function),
        ("ref`constant", re.compile(r"`([A-Z][A-Z0-9_]+)`"), format_code),
    ]
}

RE_LOCATION = re.compile(r"^#* (.*)")

index = {}

def collect_index(notebook_name):
    notebook_path = notebook_name
    fragment = ""
    title = None
    subtitle = None

    # load the notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)

    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            for match in RE_LOCATION.findall(cell.source):
                if title is None:
                    title = match
                else:
                    subtitle = match
                fragment = title_to_fragment(match)
            
        for (tp, regex, formatter) in ITEMS.get(cell.cell_type, []):
            for match in regex.findall(cell.source):
                entry = formatter(match)
                if entry not in index:
                    index[entry] = []

                link = notebook_name + fragment
                listed_title = title
                if subtitle is not None:
                    listed_title += " (" + subtitle + ")"
                index[entry].append((listed_title, link))
                
def index_key(entry):
    s = entry.upper()
    while len(s) > 0 and s[0] not in string.ascii_letters:
        s = s[1:]
    return s if len(s) > 0 else entry

def index_markdown():
    s = ""
    entries = list(index.keys())
    entries.sort(key=index_key)
    current_letter = None
    for entry in entries:
        
        entry_letter = index_key(entry)[0]
        if entry_letter != current_letter:
            if current_letter is not None:
                s += "\n"
            current_letter = entry_letter
            s += "## " + entry_letter + "\n"

        s += "* " + entry + " - "

        occurrences = index[entry]
        s += ", ".join(["[" + title + "](" + link + ")" for title, link in occurrences])
        s += "\n"

    return s

if __name__ == "__main__":
    index = {}
    for notebook in sys.argv[1:]:
        collect_index(notebook)
    index_str = index_markdown()
    
    title = "# Index"
    index_notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell(source=title),
            nbformat.v4.new_markdown_cell(source=index_str),
        ])
    
    sys.stdout.buffer.write(nbformat.writes(index_notebook).encode('utf-8'))
