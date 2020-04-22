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

import asyncio
import json
import os
import tempfile

import concurrent.futures

import nbconvert

from pyppeteer import launch

from traitlets import default

import pikepdf

from nbconvert.exporters import Exporter


async def html_to_pdf(html_file, pdf_file):
    """Convert a HTML file to a PDF"""
    browser = await launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
    page = await browser.newPage()
    await page.setViewport(dict(width=640, height=640))
    
    # We use 'print' as media type to avoid having the menu clutter things
    await page.emulateMedia("print")

    await page.goto(f"file:///{html_file}", {"waitUntil": ["networkidle2"]})

    page_margins = {
        "left": "0px",
        "right": "0px",
        "top": "0px",
        "bottom": "0px",
    }

    dimensions = await page.evaluate(
        """() => {
        return {
            width: document.body.scrollWidth,
            height: document.body.scrollHeight,
            offsetHeight: document.body.offsetHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }"""
    )
    width = dimensions["width"]
    height = dimensions["height"]

    await page.addStyleTag(
        {
            "content": """
                #notebook-container {
                    box-shadow: none;
                    padding: unset
                }
                div.cell {
                    page-break-inside: avoid;
                }
                div.output_wrapper {
                    page-break-inside: avoid;
                }
                div.output {
                    page-break-inside: avoid;
                }
         """
        }
    )

    await page.pdf(
        {
            "path": pdf_file,
            "width": width,
            # Adobe can not display pages longer than 200inches. So we limit
            # ourselves to that and start a new page if needed.
            "height": min(height, 200 * 72),
            "printBackground": True,
            "margin": page_margins,
        }
    )

    await browser.close()


def attach_notebook(pdf_in, pdf_out, notebook):
    N = pikepdf.Name

    main_pdf = pikepdf.open(pdf_in)

    the_file = pikepdf.Stream(main_pdf, notebook["contents"])
    the_file[N("/Type")] = N("/EmbeddedFile")

    file_wrapper = pikepdf.Dictionary(F=the_file)

    fname = notebook["file_name"]
    embedded_file = pikepdf.Dictionary(
        Type=N("/Filespec"), UF=fname, F=fname, EF=file_wrapper
    )

    name_tree = pikepdf.Array([pikepdf.String(fname), embedded_file])

    embedded_files = pikepdf.Dictionary(Names=name_tree)

    names = pikepdf.Dictionary(EmbeddedFiles=embedded_files)

    main_pdf.Root[N("/Names")] = names

    main_pdf.save(pdf_out)


async def notebook_to_pdf(notebook, pdf_path, config=None, resources=None, **kwargs):
    """Convert a notebook to PDF"""
    if config is None:
        config = {}
    exporter = nbconvert.HTMLExporter(config=config)
    exported_html, _ = exporter.from_notebook_node(
        notebook, resources=resources, **kwargs
    )

    with tempfile.NamedTemporaryFile(suffix=".html") as f:
        f.write(exported_html.encode())
        f.flush()
        await html_to_pdf(f.name, pdf_path)


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