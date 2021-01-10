#!/usr/bin/env python

import io, os, sys, types, re
import datetime

# from IPython import get_ipython
# from IPython.core.interactiveshell import InteractiveShell

import nbformat
from import_notebooks import RE_CODE

# Things to ignore in exported Python code
RE_IGNORE = re.compile(r'^get_ipython().*|^%.*')
RE_IMPORT_BOOKUTILS = re.compile(r'^import bookutils.*$', re.MULTILINE)
RE_FROM_BOOKUTILS = re.compile(r'^from bookutils import .*$', re.MULTILINE)

# Things to import only if main (reduces dependencies)
RE_IMPORT_IF_MAIN = re.compile(r'^(from|import)[ \t]+(matplotlib|mpl_toolkits|numpy|scipy|IPython|requests|FTB|Collector|bookutils import YouTubeVideo).*$', re.MULTILINE)

# Strip blank lines
RE_BLANK_LINES = re.compile(r'^[ \t]*$', re.MULTILINE)

# Comments
RE_COMMENTS = re.compile(r'^#.*$', re.MULTILINE)

# Common header for all code
HEADER = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "{title}".
# Web site: https://www.{project}.org/html/{module}.html
# Last change: {timestamp}
#
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# Replacement for "import bookutils"
SET_FIXED_SEED = r"""# We use the same fixed seed as the notebook to ensure consistency
import random
random.seed(2001)"""

def is_all_comments(code):
    executable_code = re.sub(RE_COMMENTS, '', code).strip()
    return executable_code == ""

def is_triple_quote(s):
    return s == '"""' or s == "'''"

def prefix_code(code, prefix):
    out = prefix
    quote = ''

    for i, c in enumerate(code):
        if c == '\n' and not quote:  # do not indent quotes
            out += '\n' + prefix
        else:
            out += c

        if i < len(code) - 3:
            next_three = str(code[i:i+3])
            if not quote and is_triple_quote(next_three):
                quote = next_three  # start of quote
            elif next_three == quote:
                quote = ''  # end of quote

    return out

def indent_code(code):
    lines = prefix_code(code, "    ")
    return re.sub(RE_BLANK_LINES, '', lines)


def fix_imports(code):
    # For proper packaging, we must import our modules from the local dir
    # Our modules all start with an upper-case letter

    if code.startswith("from IPython"):
        # IPython
        return code

    if code.find(r"\bCollector\b") >= 0 or code.find(r"\bFTB\b") >= 0:
        # FuzzManager imports
        return code

    code = re.sub(r"^from *([A-Z].*|bookutils.*)$",
r'''if __package__ is None or __package__ == "":
    from \1
else:
    from .\1
''', code, flags=re.MULTILINE)

    code = re.sub(r"^import *([A-Z].*|bookutils.*)$",
r'''if __package__ is None or __package__ == "":
    import \1
else:
    from . import \1
''', code, flags=re.MULTILINE)

    return code

def first_line(text):
    index = text.find('\n')
    if index >= 0:
        return text[:index]
    else:
        return text

def print_utf8(s):
    sys.stdout.buffer.write(s.encode('utf-8'))
    
def decode_title(s):
    # We have non-breaking spaces in some titles
    return s.replace('\xa0', ' ')

def print_if_main(code):
    # Run code only if run as main file
    print_utf8('\nif __name__ == "__main__":\n')
    print_utf8(indent_code(code) + "\n\n")

def export_notebook_code(notebook_name, project="fuzzingbook", path=None):
    # notebook_path = import_notebooks.find_notebook(notebook_name, path)
    notebook_path = notebook_name

    if project == "debuggingbook":
        title = "The Debugging Book"
    else:
        title = "The Fuzzing Book"

    # load the notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)

    # shell = InteractiveShell.instance()

    # Get versioning info
    notebook_modification_time = os.path.getmtime(notebook_path)    
    timestamp = datetime.datetime.fromtimestamp(notebook_modification_time) \
        .astimezone().isoformat(sep=' ', timespec='seconds')
    module = os.path.splitext(os.path.basename(notebook_name))[0]

    header = HEADER.format(module=module, 
                           timestamp=timestamp,
                           project=project,
                           title=title)
    print_utf8(header)
    sep = ''

    for cell in notebook.cells:
        if cell.cell_type == 'code':
            code = cell.source
                
            while code.startswith('#') or code.startswith('\n'):
                # Skip leading comments
                if code.find('\n') >= 0:
                    code = code[code.find('\n') + 1:]
                else:
                    code = ''

            if len(code.strip()) == 0:
                # Empty code
                continue
            
            bang = False
            if code.startswith('!'):
                code = "import os\nos.system(f" + repr(code[1:]) + ")"
                bang = True

            if RE_IMPORT_BOOKUTILS.match(code):
                # Don't import all of bookutils (requires nbformat & Ipython)
                print_if_main(SET_FIXED_SEED)
            elif RE_IMPORT_IF_MAIN.match(code):
                print_if_main(code)
            elif RE_FROM_BOOKUTILS.match(code):
                # This would be "from bookutils import HTML"
                # print ("Code: ", repr(code))
                code = fix_imports(code)
                print_utf8("\n" + code + "\n")
            elif RE_IGNORE.match(code):
                # Code to ignore - comment out
                print_utf8("\n" + prefix_code(code, "# ") + "\n")
            elif RE_CODE.match(code) and not bang:
                # imports and defs
                code = fix_imports(code)
                print_utf8("\n" + code + "\n")
            elif is_all_comments(code):
                # Only comments
                print_utf8("\n" + code + "\n")
            else:
                print_if_main(code)
        else:
            # Anything else
            contents = cell.source
            if contents.startswith('#'):
                # Header
                line = first_line(contents)
                print_utf8("\n" + prefix_code(decode_title(line), "# ") + "\n")
                print_if_main("print(" + repr(sep + decode_title(line)) + ")\n\n")
                sep = '\n'
            else:
                # We don't include contents, as they fall under a different license
                # print_utf8("\n" + prefix_code(contents, "# ") + "\n")
                pass

if __name__ == "__main__":
    args = sys.argv
    project = 'fuzzingbook'

    if len(args) > 2 and args[1] == '--project':
        project = args[2]
        args = args[3:]
    else:
        args = args[1:]
        
    for notebook in args:
        export_notebook_code(notebook, project=project)
