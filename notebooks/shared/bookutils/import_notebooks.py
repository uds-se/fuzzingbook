#!/usr/bin/env python
# Settings and definitions for fuzzingbook notebooks

# We want to import notebooks as modules
# Source: http://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html

import io, os, sys, types, re
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell
from importlib.abc import MetaPathFinder

import linecache
import ast

from typing import Optional, List, Any, Dict

# To avoid re-running notebook computations during import,
# we only import code cells that match this regular expression
# i.e. definitions of 
# * functions: `def func()`
# * classes: `class X:`
# * constants: `UPPERCASE_VARIABLES`
# * types: `TypeVariables`, and
# * imports: `import foo`
#
# PLEASE NOTE: if you change this, also change the corresponding 
# definition in utils/export_notebook_code.py
RE_CODE = re.compile(r"^(def |class |@|[A-Z][A-Za-z0-9_]+ [-+*/]?= |[A-Z][A-Za-z0-9_]+[.:]|import |from )")

def do_import(code: str) -> bool:
    """Return True if code is to be exported"""
    while code.startswith('#') or code.startswith('\n'):
        # Skip leading comments
        code = code[code.find('\n') + 1:]

    return RE_CODE.match(code) is not None

assert do_import("def foo():\n    pass")
assert do_import("# ignore\ndef foo():\n    pass")
assert do_import("# ignore\nclass Bar:\n    pass")
assert do_import("XYZ = 123")
assert not do_import("xyz = 123")
assert not do_import("foo()")

def find_notebook(fullname: str, path: Optional[List[str]] = None) -> Optional[str]:
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit('.', 1)[-1]
    if not path:
        path = sys.path
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path

    return None

class NotebookLoader:
    """Module Loader for Jupyter Notebooks"""
    def __init__(self, path: Optional[List[str]] = None) -> None:
        self.shell = InteractiveShell.instance()
        self.path = path
        self.lines: Dict[str, str] = {}

    def load_module(self, fullname: str) -> types.ModuleType:
        self.lines[fullname] = ''
        """import a notebook as a module"""
        path = find_notebook(fullname, self.path)
        if path is None:
            raise FileNotFoundError(f"Can't find {fullname}")

        # print ("importing Jupyter notebook from %s" % path)

        # load the notebook object
        with io.open(path, 'r', encoding='utf-8') as f:
            nb = read(f, 4)

        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(fullname)
        mod.__file__ = path
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython
        sys.modules[fullname] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        codecells = [self.shell.input_transformer_manager.transform_cell(cell.source)
                              for cell in nb.cells if cell.cell_type == 'code']
        source = [code for code in codecells if do_import(code)]

        lno = 1

        try:
            for code in source:
                parsed = ast.parse(code, filename=path, mode='exec')
                ast.increment_lineno(parsed, n=lno - 1)
                exec(compile(parsed, path, 'exec'), mod.__dict__)
                lno += len(code.split('\n'))
            self.lines[fullname] = '\n'.join(source)
            p = len(self.lines[fullname].split('\n')) + 1
            assert lno == p
    
        finally:
            self.shell.user_ns = save_user_ns
            data = self.lines[fullname]
            linecache.cache[path] = (len(data), None,   # type: ignore
                                    [line+'\n' for line in data.splitlines()],
                                    fullname)
        return mod

class NotebookFinder(MetaPathFinder):
    """Module finder that locates Jupyter Notebooks"""
    def __init__(self) -> None:
        self.loaders: Dict[Any, Any] = {}

    def find_module(self, fullname: str, path: Any = None) -> Any:
        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)
        return self.loaders[key]

sys.meta_path.append(NotebookFinder())
