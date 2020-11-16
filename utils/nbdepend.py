#!/usr/bin/env python
# Issue dependencies for given notebook(s)
"""
usage:

python nbdepend.py A.ipynb B.ipynb C.ipynb > Makefile_deps
"""

import io, os, sys, types, re

from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

import nbformat
import argparse

from graphviz import Digraph, Source

RE_IMPORT = re.compile(r"^ *import  *([a-zA-Z0-9_]+)", re.MULTILINE)
RE_FROM = re.compile(r"^ *from  *([a-zA-Z0-9_]+)  *import", re.MULTILINE)


def notebook_dependencies(notebook_name, include_minor_dependencies=True, path=None):
    # notebook_path = import_notebooks.find_notebook(notebook_name, path)
    notebook_path = notebook_name

    # load the notebook
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, 4)

    shell = InteractiveShell.instance()

    modules = set()
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            # transform the input to executable Python
            code = shell.input_transformer_manager.transform_cell(cell.source)
            if not include_minor_dependencies and code.find('# minor') >= 0:
                continue
            for match in re.finditer(RE_IMPORT, code):
                modules.add(match.group(1))
            for match in re.finditer(RE_FROM, code):
                modules.add(match.group(1))

    return modules

def print_notebook_dependencies(notebooks):
    for notebook_name in notebooks:
        for module in notebook_dependencies(notebook_name):
            print(module)


def get_title(notebook):
    """Return the title from a notebook file"""
    contents = get_text_contents(notebook)
    match = re.search(r'^# (.*)', contents, re.MULTILINE)
    if match is None:
        print(notebook + ": no title", file=sys.stderr)
        return notebook

    title = match.group(1).replace(r'\n', '')
    # print("Title", title.encode('utf-8'))
    return title

def get_text_contents(notebook):
    with io.open(notebook, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    contents = ""
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            contents += "".join(cell.source) + "\n\n"
            
    # print("Contents of", notebook, ": ", repr(contents[:100]))

    return contents

   
def draw_notebook_dependencies(notebooks, 
    format='svg', transitive_reduction=True, clusters=True, project='fuzzingbook'):
    dot = Digraph(comment="Notebook dependencies")
    # dot.attr(size='20,30', rank='max')
    
    if project == 'debuggingbook':
        fontname = 'Raleway'
        fontcolor = 'purple'
    else:
        fontname = 'Patua One'
        fontcolor = '#B03A2E'
    
    node_attrs = {
        'shape': 'note',  # note, plain, none
        'style': 'filled',
        'fontname': fontname,
        'fontcolor': fontcolor,
        'fillcolor': 'white'
    }
    cluster = None

    cluster_attrs = {
        'shape': 'plain',  # note, plain, none
        'style': 'filled',
        'fontname': fontname,
        'fontcolor': 'black',
        'color': '#F0F0F0',
    }

    for notebook_name in notebooks:
        dirname = os.path.dirname(notebook_name)
        basename = os.path.splitext(os.path.basename(notebook_name))[0]
        title = get_title(notebook_name)
        if clusters:
            if title.startswith("Part"):
                if cluster is not None:
                    cluster.attr(**cluster_attrs)
                    dot.subgraph(cluster)

                cluster = Digraph(name='cluster_' + basename)
                cluster.node(basename, label=title, URL='%s.ipynb' % basename,
                tooltip=basename, shape='plain', fontname=fontname)
            
            elif cluster is not None:
                cluster.node(basename)

        for module in notebook_dependencies(notebook_name,
                 include_minor_dependencies=False):
            module_file = os.path.join(dirname, module + ".ipynb")
            if module_file in notebooks:
                module_title = get_title(module_file)
                dot.node(basename, URL='%s.ipynb' % basename, 
                    label=title, tooltip=basename, **node_attrs)
                dot.node(module, URL='%s.ipynb' % module, 
                    label=module_title, tooltip=module, **node_attrs)
                dot.edge(module, basename)
                
    if cluster is not None:
        cluster.attr(**cluster_attrs)
        dot.subgraph(cluster)
    
    if transitive_reduction:
        dot.format = 'gv'
        dot.save('depend.gv')
        os.system('tred depend.gv > depend.gv~ && mv depend.gv~ depend.gv')
        dot = Source.from_file('depend.gv')
        os.remove('depend.gv')

    dot.format = format
    dot.render('depend')
    os.system('cat depend.' + format)
    os.remove('depend')
    os.remove('depend.' + format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", action='store_true', help="Produce graph")
    parser.add_argument("--graph-format", action='store', default='svg', help="Graph format (gv, pdf, svg, ...)")
    parser.add_argument("--project", action='store', help="Project name")
    parser.add_argument("--transitive-reduction", action='store_true', help="Use transitive reduction")
    parser.add_argument("--cluster-by-parts", action='store_true', help="Cluster by parts")
    parser.add_argument("notebooks", nargs='*', help="notebooks to determine dependencies from")
    args = parser.parse_args()

    if args.graph:
        draw_notebook_dependencies(args.notebooks, args.graph_format, args.transitive_reduction, args.cluster_by_parts, args.project)
    else:
        print_notebook_dependencies(args.notebooks)
