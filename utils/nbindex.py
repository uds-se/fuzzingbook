#!/usr/bin/env python
# Produce index for given notebook(s)
"""
usage:

python nbindex.py A.ipynb B.ipynb C.ipynb
"""


import io
import os
import sys
import types
import re
import nbformat
import string

emph_seen = False


def format_code(s):
    return "`" + s + "`"


def format_function(s):
    return format_code(s + "()")


def format_class(s):
    return format_code(s) + " class"


def format_method(s):
    # return format_code(s + "()") + " method"
    return format_function(s)


def format_emph(s):
    global emph_seen
    emph_seen = True
    return "_" + s + "_"


def format_emph_index(s):
    return s


def title_to_fragment(s):
    return "#" + s.replace(" ", "-")


ITEMS = {
    'code': [
        ("function", re.compile(
            r"^def +([A-Za-z0-9_]+)", re.MULTILINE), format_function),
        ("class",    re.compile(
            r"^class +([A-Za-z0-9_]+)", re.MULTILINE), format_class),
        ("method",   re.compile(
            r"^ +def +([A-Za-z0-9_]+)", re.MULTILINE), format_method),
        ("constant", re.compile(
            r"^ *([A-Z][A-Z0-9_]+) += ", re.MULTILINE), format_code)
    ],
    'markdown': [
        # ("_term_", re.compile(r"[^_]_([a-zA-Z]+)_[^_]"), format_emph),
        ("*term*", re.compile(r"[^*]\*([a-zA-Z][a-zA-Z0-9-_ ]*[a-zA-Z])\*[^*]"), format_emph_index),
        ("[link]", re.compile(r"\[(.*)]\(https?:"), format_emph_index),
        ("`function()`", re.compile(r"`([a-zA-Z0-9_]+)\(`"), format_function),
        ("`constant`", re.compile(r"`([A-Z][A-Z0-9_]+)`"), format_code),
    ]
}

RE_LOCATION = re.compile(r"^#+ (.*)")

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
                # print(match, file=sys.stderr)

        for (tp, regex, formatter) in ITEMS.get(cell.cell_type, []):
            for match in regex.findall(cell.source):
                entry = formatter(match)
                if entry not in index:
                    index[entry] = []
                    
                if title is None:
                    print(notebook_name + ": cell without title", file=sys.stderr)
                    continue

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

LETTERS_PER_SECTION = 5

def index_markdown():
    index_sections = []
    
    # Create entries, one cell per letter
    entries = list(index.keys())
    entries.sort(key=index_key)
    current_letter = None
    s = ""
    
    for entry in entries:
        if not index_key(entry):
            continue
        entry_letter = index_key(entry)[0]
        if entry_letter != current_letter:
            if s != "":
                index_sections.append(s)
                s = ""

            current_letter = entry_letter
            s = "### " + entry_letter + "\n\n"

        s += "* " + entry + " &mdash; "

        occurrences = index[entry]
        s += ", ".join(["[" + title + "](" + link +
                        ")" for title, link in occurrences])
        s += "\n"

    if s != "":
        index_sections.append(s)
    
    # Insert in-between titles
    ## A-E
    ### A
    ### B
    new_index_sections = []
    while len(index_sections) > 0:
        sublist = index_sections[:LETTERS_PER_SECTION]
        index_sections = index_sections[LETTERS_PER_SECTION:]
        first_letter = sublist[0][len("### ")]
        last_letter = sublist[-1][len("### ")]
        # Having &ndash; here breaks fragment links
        new_index_sections += ["## " + first_letter + " - " + last_letter] + sublist
    
    return new_index_sections

if __name__ == "__main__":
    index = {}
    for notebook in sys.argv[1:]:
        collect_index(notebook)
    index_sections = index_markdown()

    title = "# Index"
    
    if emph_seen:
        title += """
Please note: entries in _italics_ are listed only temporarily, as we convert terms to be indexed
with `*term*` instead of `_term_`.
    """
    index_notebook = nbformat.v4.new_notebook(
        cells=[nbformat.v4.new_markdown_cell(source=title)] +
            [nbformat.v4.new_markdown_cell(source=cell_content) for cell_content in index_sections]
        )

    index_notebook.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
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
        },
         "toc-autonumbering": False
    }

    sys.stdout.buffer.write(nbformat.writes(index_notebook).encode('utf-8'))
