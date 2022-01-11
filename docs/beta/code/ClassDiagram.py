#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Class Diagrams" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/ClassDiagram.html
# Last change: 2022-01-11 10:39:43+01:00
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
The Fuzzing Book - Class Diagrams

This file can be _executed_ as a script, running all experiments:

    $ python ClassDiagram.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.ClassDiagram import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/ClassDiagram.html

The function `display_class_hierarchy()` function shows the class hierarchy for the given class (or list of classes). 
* The keyword parameter `public_methods`, if given, is a list of "public" methods to be used by clients (default: all methods with docstrings).
* The keyword parameter `abstract_classes`, if given, is a list of classes to be displayed as "abstract" (i.e. with a cursive class name).

>>> display_class_hierarchy(D_Class, abstract_classes=[A_Class])

For more details, source, and documentation, see
"The Fuzzing Book - Class Diagrams"
at https://www.fuzzingbook.org/html/ClassDiagram.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Class Diagrams
# ==============

if __name__ == '__main__':
    print('# Class Diagrams')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Getting a Class Hierarchy
## -------------------------

if __name__ == '__main__':
    print('\n## Getting a Class Hierarchy')



import inspect

from typing import Callable, Dict, Type, Set, List, Union, Any, Tuple, Optional

def class_hierarchy(cls: Type) -> List[Type]:
    superclasses = cls.mro()
    hierarchy = []
    last_superclass_name = ""

    for superclass in superclasses:
        if superclass.__name__ != last_superclass_name:
            hierarchy.append(superclass)
            last_superclass_name = superclass.__name__

    return hierarchy

class A_Class:
    """A Class which does A thing right.
    Comes with a longer docstring."""

    def foo(self) -> None:
        """The Adventures of the glorious Foo"""
        pass

    def quux(self) -> None:
        """A method that is not used."""
        pass

class A_Class(A_Class):
    # We define another function in a separate cell.

    def second(self) -> None:
        pass

class B_Class(A_Class):
    """A subclass inheriting some methods."""

    VAR = "A variable"

    def foo(self) -> None:
        """A WW2 foo fighter."""
        pass

    def bar(self, qux: Any = None, bartender: int = 42) -> None:
        """A qux walks into a bar.
        `bartender` is an optional attribute."""
        pass

SomeType = List[Optional[Union[str, int]]]

class C_Class:
    """A class injecting some method"""

    def qux(self, arg: SomeType) -> SomeType:
        return arg

class D_Class(B_Class, C_Class):
    """A subclass inheriting from multiple superclasses.
    Comes with a fairly long, but meaningless documentation."""

    def foo(self) -> None:
        B_Class.foo(self)

class D_Class(D_Class):
    pass  # An incremental addiiton that should not impact D's semantics

if __name__ == '__main__':
    class_hierarchy(D_Class)

## Getting a Class Tree
## --------------------

if __name__ == '__main__':
    print('\n## Getting a Class Tree')



D_Class.__bases__

def class_tree(cls: Type, lowest: Type = None) -> List[Tuple[Type, List]]:
    ret = []
    for base in cls.__bases__:
        if base.__name__ == cls.__name__:
            if not lowest:
                lowest = cls
            ret += class_tree(base, lowest)
        else:
            if lowest:
                cls = lowest
            ret.append((cls, class_tree(base)))

    return ret

if __name__ == '__main__':
    class_tree(D_Class)

if __name__ == '__main__':
    class_tree(D_Class)[0][0]

if __name__ == '__main__':
    assert class_tree(D_Class)[0][0] == D_Class

def class_set(classes: Union[Type, List[Type]]) -> Set[Type]:
    if not isinstance(classes, list):
        classes = [classes]

    ret = set()

    def traverse_tree(tree: List[Tuple[Type, List]]) -> None:
        for (cls, subtrees) in tree:
            ret.add(cls)
            for subtree in subtrees:
                traverse_tree(subtrees)

    for cls in classes:
        traverse_tree(class_tree(cls))

    return ret

if __name__ == '__main__':
    class_set(D_Class)

if __name__ == '__main__':
    assert A_Class in class_set(D_Class)

if __name__ == '__main__':
    assert B_Class in class_set(D_Class)

if __name__ == '__main__':
    assert C_Class in class_set(D_Class)

if __name__ == '__main__':
    assert D_Class in class_set(D_Class)

if __name__ == '__main__':
    class_set([B_Class, C_Class])

### Getting Docs

if __name__ == '__main__':
    print('\n### Getting Docs')



A_Class.__doc__

A_Class.__bases__[0].__doc__

A_Class.__bases__[0].__name__

D_Class.foo

D_Class.foo.__doc__

A_Class.foo.__doc__

def docstring(obj: Any) -> str:
    doc = inspect.getdoc(obj)
    return doc if doc else ""

if __name__ == '__main__':
    docstring(A_Class)

if __name__ == '__main__':
    docstring(D_Class.foo)

def unknown() -> None:
    pass

if __name__ == '__main__':
    docstring(unknown)

import html

import re

def escape(text: str) -> str:
    text = html.escape(text)
    assert '<' not in text
    assert '>' not in text
    text = text.replace('{', '&#x7b;')
    text = text.replace('|', '&#x7c;')
    text = text.replace('}', '&#x7d;')
    return text

if __name__ == '__main__':
    escape("f(foo={})")

def escape_doc(docstring: str) -> str:
    DOC_INDENT = 0
    docstring = "&#x0a;".join(
        ' ' * DOC_INDENT + escape(line).strip()
        for line in docstring.split('\n')
    )
    return docstring

if __name__ == '__main__':
    print(escape_doc("'Hello\n    {You|Me}'"))

## Getting Methods and Variables
## -----------------------------

if __name__ == '__main__':
    print('\n## Getting Methods and Variables')



if __name__ == '__main__':
    inspect.getmembers(D_Class)

def class_items(cls: Type, pred: Callable) -> List[Tuple[str, Any]]:
    def _class_items(cls: Type) -> List:
        all_items = inspect.getmembers(cls, pred)
        for base in cls.__bases__:
            all_items += _class_items(base)

        return all_items

    unique_items = []
    items_seen = set()
    for (name, item) in _class_items(cls):
        if name not in items_seen:
            unique_items.append((name, item))
            items_seen.add(name)

    return unique_items

def class_methods(cls: Type) -> List[Tuple[str, Callable]]:
    return class_items(cls, inspect.isfunction)

def defined_in(name: str, cls: Type) -> bool:
    if not hasattr(cls, name):
        return False

    defining_classes = []

    def search_superclasses(name: str, cls: Type) -> None:
        if not hasattr(cls, name):
            return

        for base in cls.__bases__:
            if hasattr(base, name):
                defining_classes.append(base)
                search_superclasses(name, base)

    search_superclasses(name, cls)

    if any(cls.__name__ != c.__name__ for c in defining_classes):
        return False  # Already defined in superclass

    return True

if __name__ == '__main__':
    assert not defined_in('VAR', A_Class)

if __name__ == '__main__':
    assert defined_in('VAR', B_Class)

if __name__ == '__main__':
    assert not defined_in('VAR', C_Class)

if __name__ == '__main__':
    assert not defined_in('VAR', D_Class)

def class_vars(cls: Type) -> List[Any]:
    def is_var(item: Any) -> bool:
        return not callable(item)

    return [item for item in class_items(cls, is_var) 
            if not item[0].startswith('__') and defined_in(item[0], cls)]

if __name__ == '__main__':
    class_methods(D_Class)

if __name__ == '__main__':
    class_vars(B_Class)

def public_class_methods(cls: Type) -> List[Tuple[str, Callable]]:
    return [(name, method) for (name, method) in class_methods(cls) 
            if method.__qualname__.startswith(cls.__name__)]

def doc_class_methods(cls: Type) -> List[Tuple[str, Callable]]:
    return [(name, method) for (name, method) in public_class_methods(cls) 
            if docstring(method) is not None]

if __name__ == '__main__':
    public_class_methods(D_Class)

if __name__ == '__main__':
    doc_class_methods(D_Class)

def overloaded_class_methods(classes: Union[Type, List[Type]]) -> Set[str]:
    all_methods: Dict[str, Set[Callable]] = {}
    for cls in class_set(classes):
        for (name, method) in class_methods(cls):
            if method.__qualname__.startswith(cls.__name__):
                all_methods.setdefault(name, set())
                all_methods[name].add(cls)

    return set(name for name in all_methods if len(all_methods[name]) >= 2)

if __name__ == '__main__':
    overloaded_class_methods(D_Class)

## Drawing Class Hierarchy with Method Names
## -----------------------------------------

if __name__ == '__main__':
    print('\n## Drawing Class Hierarchy with Method Names')



from inspect import signature

import warnings

def display_class_hierarchy(classes: Union[Type, List[Type]], 
                            public_methods: Optional[List] = None,
                            abstract_classes: Optional[List] = None,
                            include_methods: bool = True,
                            include_class_vars: bool =True,
                            include_legend: bool = True,
                            types: Dict[str, Any] = {},
                            project: str = 'fuzzingbook',
                            log: bool = False) -> Any:
    """Visualize a class hierarchy.
`classes` is a Python class (or a list of classes) to be visualized.
`public_methods`, if given, is a list of methods to be shown as "public" (bold).
  (Default: all methods with a docstring)
`abstract_classes`, if given, is a list of classes to be shown as "abstract" (cursive).
  (Default: all classes with an abstract method)
`include_methods`: if True, include all methods (default)
`include_legend`: if True, include a legend (default)
`types`: type names with definitions, to be used in docs
    """
    from graphviz import Digraph  # type: ignore

    if project == 'debuggingbook':
        CLASS_FONT = 'Raleway, Helvetica, Arial, sans-serif'
        CLASS_COLOR = '#6A0DAD'  # HTML 'purple'
    else:
        CLASS_FONT = 'Patua One, Helvetica, sans-serif'
        CLASS_COLOR = '#B03A2E'

    METHOD_FONT = "'Fira Mono', 'Source Code Pro', 'Courier', monospace"
    METHOD_COLOR = 'black'

    if isinstance(classes, list):
        starting_class = classes[0]
    else:
        starting_class = classes
        classes = [starting_class]

    title = starting_class.__name__ + " class hierarchy"

    dot = Digraph(comment=title)
    dot.attr('node', shape='record', fontname=CLASS_FONT)
    dot.attr('graph', rankdir='BT', tooltip=title)
    dot.attr('edge', arrowhead='empty')
    edges = set()
    overloaded_methods: Set[str] = set()

    drawn_classes = set()

    def method_string(method_name: str, public: bool, overloaded: bool,
                      fontsize: float = 10.0) -> str:
        method_string = f'<font face="{METHOD_FONT}" point-size="{str(fontsize)}">'

        if overloaded:
            name = f'<i>{method_name}()</i>'
        else:
            name = f'{method_name}()'

        if public:
            method_string += f'<b>{name}</b>'
        else:
            method_string += f'<font color="{METHOD_COLOR}">' \
                             f'{name}</font>'

        method_string += '</font>'
        return method_string

    def var_string(var_name: str, fontsize: int = 10) -> str:
        var_string = f'<font face="{METHOD_FONT}" point-size="{str(fontsize)}">'
        var_string += f'{var_name}'
        var_string += '</font>'
        return var_string

    def is_overloaded(method_name: str, f: Any) -> bool:
        return (method_name in overloaded_methods or
                (docstring(f) is not None and "in subclasses" in docstring(f)))

    def is_abstract(cls: Type) -> bool:
        if not abstract_classes:
            return inspect.isabstract(cls)

        return (cls in abstract_classes or
                any(c.__name__ == cls.__name__ for c in abstract_classes))

    def is_public(method_name: str, f: Any) -> bool:
        if public_methods:
            return (method_name in public_methods or
                    f in public_methods or
                    any(f.__qualname__ == m.__qualname__
                        for m in public_methods))

        return bool(docstring(f))

    def class_vars_string(cls: Type, url: str) -> str:
        cls_vars = class_vars(cls)
        if len(cls_vars) == 0:
            return ""

        vars_string = f'<table border="0" cellpadding="0" ' \
                      f'cellspacing="0" ' \
                      f'align="left" tooltip="{cls.__name__}" href="#">'

        for (name, var) in cls_vars:
            if log:
                print(f"    Drawing {name}")

            var_doc = escape(f"{name} = {repr(var)}")
            tooltip = f' tooltip="{var_doc}"'
            href = f' href="{url}"'
            vars_string += f'<tr><td align="left" border="0"' \
                           f'{tooltip}{href}>'

            vars_string += var_string(name)
            vars_string += '</td></tr>'

        vars_string += '</table>'
        return vars_string

    def class_methods_string(cls: Type, url: str) -> str:
        methods = public_class_methods(cls)
        # return "<br/>".join([name + "()" for (name, f) in methods])
        if len(methods) == 0:
            return ""

        methods_string = f'<table border="0" cellpadding="0" ' \
                         f'cellspacing="0" ' \
                         f'align="left" tooltip="{cls.__name__}" href="#">'

        for public in [True, False]:
            for (name, f) in methods:
                if public != is_public(name, f):
                    continue

                if log:
                    print(f"    Drawing {name}()")

                if is_public(name, f) and not docstring(f):
                    warnings.warn(f"{f.__qualname__}() is listed as public,"
                                  f" but has no docstring")

                overloaded = is_overloaded(name, f)

                sig = str(inspect.signature(f))
                # replace 'List[Union[...]]' by the actual type def
                for tp in types:
                    tp_def = str(types[tp]).replace('typing.', '')
                    sig = sig.replace(tp_def, tp)
                sig = sig.replace('__main__.', '')

                method_doc = escape(name + sig)
                if docstring(f):
                    method_doc += ":&#x0a;" + escape_doc(docstring(f))

                if log:
                    print(f"    Method doc: {method_doc}")

                # Tooltips are only shown if a href is present, too
                tooltip = f' tooltip="{method_doc}"'
                href = f' href="{url}"'
                methods_string += f'<tr><td align="left" border="0"' \
                                  f'{tooltip}{href}>'

                methods_string += method_string(name, public, overloaded)

                methods_string += '</td></tr>'

        methods_string += '</table>'
        return methods_string

    def display_class_node(cls: Type) -> None:
        name = cls.__name__

        if name in drawn_classes:
            return
        drawn_classes.add(name)

        if log:
            print(f"Drawing class {name}")

        if cls.__module__ == '__main__':
            url = '#'
        else:
            url = cls.__module__ + '.ipynb'

        if is_abstract(cls):
            formatted_class_name = f'<i>{cls.__name__}</i>'
        else:
            formatted_class_name = cls.__name__

        if include_methods or include_class_vars:
            vars = class_vars_string(cls, url)
            methods = class_methods_string(cls, url)
            spec = '<{<b><font color="' + CLASS_COLOR + '">' + \
                formatted_class_name + '</font></b>'
            if include_class_vars and vars:
                spec += '|' + vars
            if include_methods and methods:
                spec += '|' + methods
            spec += '}>'
        else:
            spec = '<' + formatted_class_name + '>'

        class_doc = escape('class ' + cls.__name__)
        if docstring(cls):
            class_doc += ':&#x0a;' + escape_doc(docstring(cls))
        else:
            warnings.warn(f"Class {cls.__name__} has no docstring")

        dot.node(name, spec, tooltip=class_doc, href=url)

    def display_class_trees(trees: List[Tuple[Type, List]]) -> None:
        for tree in trees:
            (cls, subtrees) = tree
            display_class_node(cls)

            for subtree in subtrees:
                (subcls, _) = subtree

                if (cls.__name__, subcls.__name__) not in edges:
                    dot.edge(cls.__name__, subcls.__name__)
                    edges.add((cls.__name__, subcls.__name__))

            display_class_trees(subtrees)

    def display_legend() -> None:
        fontsize = 8.0

        label = f'<b><font color="{CLASS_COLOR}">Legend</font></b><br align="left"/>' 

        for item in [
            method_string("public_method",
                          public=True, overloaded=False, fontsize=fontsize),
            method_string("private_method",
                          public=False, overloaded=False, fontsize=fontsize),
            method_string("overloaded_method",
                          public=False, overloaded=True, fontsize=fontsize)
        ]:
            label += '&bull;&nbsp;' + item + '<br align="left"/>'

        label += f'<font face="Helvetica" point-size="{str(fontsize + 1)}">' \
                 'Hover over names to see doc' \
                 '</font><br align="left"/>'

        dot.node('Legend', label=f'<{label}>', shape='plain', fontsize=str(fontsize + 2))

    for cls in classes:
        tree = class_tree(cls)
        overloaded_methods = overloaded_class_methods(cls)
        display_class_trees(tree)

    if include_legend:
        display_legend()

    return dot

if __name__ == '__main__':
    display_class_hierarchy(D_Class, types={'SomeType': SomeType},
                            project='debuggingbook', log=True)

if __name__ == '__main__':
    display_class_hierarchy(D_Class, types={'SomeType': SomeType},
                            project='fuzzingbook')

if __name__ == '__main__':
    display_class_hierarchy([A_Class, B_Class],
                            abstract_classes=[A_Class],
                            public_methods=[
                                A_Class.quux,
                            ],
                            log=True)

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    display_class_hierarchy(D_Class, abstract_classes=[A_Class])

## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')


