#!/usr/bin/env python

import io, os, sys, types, re
import datetime
from typing import Dict, Optional, List, Any, Tuple

from bs4 import BeautifulSoup  # type: ignore

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

# "{title}" - a chapter of "{booktitle}"
# Web site: https://www.{project}.org/html/{module}.html
# Last change: {timestamp}
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

r'''
{booktitle} - {title}

This file can be _executed_ as a script, running all experiments:

    $ python {module}.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from {project}.{module} import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.{project}.org/html/{module}.html

{synopsis}
For more details, source, and documentation, see
"{booktitle} - {title}"
at https://www.{project}.org/html/{module}.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = '{project}'

"""

# Replacement for "import bookutils"
SET_FIXED_SEED = r"""# We use the same fixed seed as the notebook to ensure consistency
import random
random.seed(2001)"""

RE_PIC = r'(\n)+![[].*(\n)+'

def fix_synopsis(s: str) -> str:
    s = s.replace('```python\n', '')
    s = s.replace('```', '')
    s = s[s.find(".\n\n") + 3:]
    s = re.sub(RE_PIC, '\n', s, flags=re.MULTILINE)
    s = BeautifulSoup(s, "lxml").text
    return s

def is_all_comments(code: str) -> bool:
    executable_code = re.sub(RE_COMMENTS, '', code).strip()
    return executable_code == ""

def is_triple_quote(s: str) -> bool:
    return s == '"""' or s == "'''"

def prefix_code(code: str, prefix: str) -> str:
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

def indent_code(code: str) -> str:
    lines = prefix_code(code, "    ")
    return re.sub(RE_BLANK_LINES, '', lines)

def fix_imports(code: str) -> str:
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
current_class: Optional[str] = None

RE_SUBCLASS = re.compile(r'^class ([A-Z][^(:]*)[(:]')
RE_SUBCLASS_SELF = re.compile(r'^class ([A-Z].*)\(\1\):$', flags=re.MULTILINE)

def fix_subclass_self(code: str) -> str:
    if not mypy:
        return code

    match = RE_SUBCLASS.search(code)
    if match:
        class_name = match.group(1)
        
        global current_class
        if class_name == current_class:
            # Add body to current class definition
            old_class_name = class_name
            code = RE_SUBCLASS_SELF.sub('', code)
        elif class_name in class_renamings:
            old_class_name = f'{class_name}_{class_renamings[class_name]}'
            class_renamings[class_name] += 1
        else:
            old_class_name = class_name
            class_renamings[class_name] = 1

        new_class_name = f'{class_name}_{class_renamings[class_name]}'
            
        code = code.replace(f'class {class_name}({class_name}',
                            f'class __NEW_CLASS__(__OLD_CLASS__')
        current_class = class_name

    else:
        # No match
        current_class = None

    for cls_name in class_renamings:
        new_cls_name = f'{cls_name}_{class_renamings[cls_name]}'
        code = re.sub(fr"\b{cls_name}\b", new_cls_name,
                      code, flags=re.MULTILINE)

    if match:
        code = code.replace('__NEW_CLASS__', new_class_name)
        code = code.replace('__OLD_CLASS__', old_class_name)
        code = code.replace('__CLASS__', class_name)

    return code
    
def fix_code(code: str) -> str:
    return fix_subclass_self(code)

def first_line(text: str) -> str:
    index = text.find('\n')
    if index >= 0:
        return text[:index]
    else:
        return text

def print_utf8(s: str) -> None:
    sys.stdout.buffer.write(s.encode('utf-8'))

def decode_title(s: str) -> str:
    # We have non-breaking spaces in some titles
    return s.replace('\xa0', ' ')
    
def split_title(s: str) -> Tuple[str, str]:
    """Split a title into hashes and text"""
    list = s.split(' ', 1)
    return list[0], list[1]

def print_if_main(code: str) -> None:
    # Run code only if run as main file
    if mypy:
        print_utf8('\n' + code + '\n')
    else:
        print_utf8("\nif __name__ == '__main__':\n")
        print_utf8(indent_code(code) + "\n")
        
def get_notebook_synopsis(notebook_name: str, 
                          path: Optional[List[str]] = None) -> Tuple[Optional[str], str]:
    notebook_path = notebook_name

    title = None
    synopsis = ""

    # load the notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)
    
    for cell in notebook.cells:
        if cell.cell_type != 'markdown':
            continue

        contents = cell.source
        if not title and contents.startswith('# '):
            lines = contents.splitlines()
            _, title = split_title(lines[0])

        if not synopsis and contents.startswith('## Synopsis'):
            synopsis = contents
            
        if title and synopsis:
            break
            
    return title, fix_synopsis(synopsis)
    
def export_notebook_code(notebook_name: str, 
                         project: str = "fuzzingbook",
                         path: Optional[List[str]] = None) -> None:
    # notebook_path = import_notebooks.find_notebook(notebook_name, path)
    notebook_path = notebook_name
    
    title, synopsis = get_notebook_synopsis(notebook_name, path)

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
                           booktitle=booktitle,
                           title=title,
                           synopsis=synopsis)

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
            if mypy:
                pass
            elif contents.startswith('#'):
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
                
    if mypy:
        print_utf8('\n# Original class names\n')
        for class_name in class_renamings:
            print_utf8(f'{class_name} = {class_name}_{class_renamings[class_name]}\n')

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
