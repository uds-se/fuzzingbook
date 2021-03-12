#!/usr/bin/env python
r"""revel.js slides in the ipypublish format, preprocessed with default metadata tags;
- removes code cells, unless set otherwise
- resolves or removes (if no converter) latex tags (like \cite{abc}, \ref{})
- splits titles and sub-titles into separate slides
"""

from ipypublish.filters.replace_string import replace_string
from ipypublish.html.create_tpl import create_tpl
from ipypublish.html.ipypublish import latex_doc
from ipypublish.html.ipypublish import slides_mkdown
from ipypublish.html.standard import content
from ipypublish.html.standard import content_tagging
from ipypublish.html.standard import mathjax
from ipypublish.html.standard import slides
from ipypublish.html.standard import widgets
from ipypublish.preprocessors.latex_doc_captions import LatexCaptions
from ipypublish.preprocessors.latex_doc_defaults import MetaDefaults
from ipypublish.preprocessors.latex_doc_html import LatexDocHTML
from ipypublish.preprocessors.latex_doc_links import LatexDocLinks
from ipypublish.preprocessors.latextags_to_html import LatexTagsToHTML

oformat = 'Slides'

_filters = {'replace_string': replace_string}

cell_defaults = {
    "ipub": {
        "figure": {
            "placement": "H"
        },
        "table": {
            "placement": "H"
        },
        "equation": True,
        "text": True,
        "mkdown": True,
        "code": False,
        "error": False
    }
}

nb_defaults = {
    "ipub": {
        "titlepage": {},
        "toc": True,
        "listfigures": False,
        "listtables": False,
        "listcode": False,
    }
}

config = {'TemplateExporter.filters': _filters,
          'Exporter.filters': _filters,
          'Exporter.preprocessors': [MetaDefaults, LatexDocLinks, LatexDocHTML, LatexTagsToHTML, LatexCaptions],
          'SplitOutputs.split': True,
          'MetaDefaults.cell_defaults': cell_defaults,
          'MetaDefaults.nb_defaults': nb_defaults}

template = create_tpl([
    content.tpl_dict, content_tagging.tpl_dict,
    mathjax.tpl_dict, widgets.tpl_dict,
    slides.tpl_dict, latex_doc.tpl_dict, slides_mkdown.tpl_dict,

])
