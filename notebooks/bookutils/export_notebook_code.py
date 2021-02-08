#!/usr/bin/env python

import io, os, sys, types, re
import datetime
from typing import Dict

# from IPython import get_ipython
# from IPython.core.interactiveshell import InteractiveShell

import nbformat
from import_notebooks import RE_CODE  # type: ignore

# If True, create mypy-friendly code
mypy = False

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

# This material is part of "{booktitle}".
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


# This file is generated automatically.
# It can be executed as a script, running all experiments:
#
#     $ python {module}.py
#
# or imported as a package, providing classes, functions, and constants:
#
#     >>> import {project}.{module}
#
# For details, source, and documentation, see "{booktitle}" chapter at 
# https://www.{project}.org/html/{module}.html


# Allow to use 'from . import <module>' when run as script (see PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = '{project}'

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
    
    if mypy:
        return code

    if code.startswith("from IPython"):
        # IPython
        return code

    if code.find(r"\bCollector\b") >= 0 or code.find(r"\bFTB\b") >= 0:
        # FuzzManager imports
        return code

    code = re.sub(r"^from *([A-Z].*|bookutils.*)$", 
                  r'from .\1', code, flags=re.MULTILINE)

    code = re.sub(r"^import *([A-Z].*|bookutils.*)$",
                  r'from . import \1', code, flags=re.MULTILINE)

    return code
    
class_renamings: Dict[str, int] = {}

RE_SUBCLASS_SELF = re.compile(r'class ([A-Z].*)\(\1')
def fix_subclass_self(code):
    if not mypy:
        return code
        
    match = RE_SUBCLASS_SELF.search(code)
    if match:
        class_name = match.group(1)
        if class_name in class_renamings:
            old_class_name = f'{class_name}_{class_renamings[class_name]}'
            class_renamings[class_name] += 1
        else:
            old_class_name = class_name
            class_renamings[class_name] = 1
            
        new_class_name = f'{class_name}_{class_renamings[class_name]}'
            
        code = code.replace(f'class {class_name}({class_name}',
                            f'class __NEW_CLASS__(__OLD_CLASS__')
        code += f'\n\n__CLASS__ = __NEW_CLASS__  # type: ignore'

    for cls_name in class_renamings:
        new_cls_name = f'{cls_name}_{class_renamings[cls_name]}'
        code = re.sub(fr"\b{cls_name}\b", new_cls_name,
                      code, flags=re.MULTILINE)

    if match:
        code = code.replace('__NEW_CLASS__', new_class_name)
        code = code.replace('__OLD_CLASS__', old_class_name)
        code = code.replace('__CLASS__', class_name)

    return code
    
def fix_code(code):
    return fix_subclass_self(code)

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
    
def split_title(s):
    """Split a title into hashes and text"""
    list = s.split(' ', 1)
    return list[0], list[1]

def print_if_main(code):
    # Run code only if run as main file
    if mypy:
        print_utf8(code + '\n\n')
    else:
        print_utf8("\nif __name__ == '__main__':\n")
        print_utf8(indent_code(code) + "\n\n")
    
def export_notebook_code(notebook_name, project="fuzzingbook", path=None):
    # notebook_path = import_notebooks.find_notebook(notebook_name, path)
    notebook_path = notebook_name

    if project == "debuggingbook":
        booktitle = "The Debugging Book"
    else:
        booktitle = "The Fuzzing Book"

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
                           booktitle=booktitle)
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
                code = fix_imports(code)
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
                # imports, classes, and defs
                code = fix_imports(code)
                code = fix_code(code)
                print_utf8("\n" + code + "\n")
            elif is_all_comments(code):
                # Only comments
                print_utf8("\n" + code + "\n")
            else:
                # Regular code
                code = fix_code(code)
                print_if_main(code)
        else:
            # Anything else
            contents = cell.source
            if contents.startswith('#'):
                # Header
                line = first_line(contents)
                decoded_title = decode_title(line)
                hashes, text = split_title(decoded_title)
                underline = '=' if hashes == '#' else '-'
                print_utf8("\n")
                print_utf8(prefix_code(decoded_title, "") + "\n")
                if len(hashes) <= 2:
                    print_utf8('#' * len(hashes) + ' ' + 
                               underline * len(text) + '\n')
                print_if_main("print(" + repr(sep + decoded_title) + ")\n\n")
                sep = '\n'
            else:
                # We don't include contents, as they fall under a different license
                # print_utf8("\n" + prefix_code(contents, "# ") + "\n")
                pass

if __name__ == '__main__':
    args = sys.argv
    project = 'fuzzingbook'

    if len(args) > 2 and args[1] == '--project':
        project = args[2]
        args = args[3:]
    else:
        args = args[1:]
    
    if len(args) > 1 and args[0] == '--mypy':
        mypy = True
        args = args[1:]
    else:
        mypy = False

    for notebook in args:
        export_notebook_code(notebook, project=project)
