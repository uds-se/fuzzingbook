#!/usr/bin/env python
# Convert HTML file into PDF with notebook attached
"""
usage:

python htmltonbpdf.py /PATH/TO/X.html X.ipynb X.pdf
"""

import argparse
import asyncio
import tempfile

# From https://github.com/betatim/notebook-as-pdf
from notebook_as_pdf import html_to_pdf, attach_notebook

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("html", help="Notebook rendered as HTML")
    parser.add_argument("notebook", help="Notebook source (to be attached)")
    parser.add_argument("pdf", help="Notebook PDF output")
    args = parser.parse_args()
    
    # print(repr(args.html))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        loop.run_until_complete(html_to_pdf(args.html, f.name))
        
        notebook = {}
        notebook["file_name"] = args.notebook
        notebook["contents"] = open(args.notebook, "rb").read()
        
        attach_notebook(f.name, args.pdf, notebook)