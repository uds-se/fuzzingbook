#!/usr/bin/env python
r"""revel.js slides in the ipypublish format;
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
from ipypublish.preprocessors.latex_doc_html import LatexDocHTML
from ipypublish.preprocessors.latex_doc_links import LatexDocLinks
from ipypublish.preprocessors.latextags_to_html import LatexTagsToHTML

oformat = 'Slides'

_filters = {'replace_string': replace_string}

config = {'TemplateExporter.filters': _filters,
          'Exporter.filters': _filters,
          'Exporter.preprocessors': [LatexDocLinks, LatexDocHTML, LatexTagsToHTML, LatexCaptions]}

template = create_tpl([
    content.tpl_dict, content_tagging.tpl_dict,
    mathjax.tpl_dict, widgets.tpl_dict,
    slides.tpl_dict, latex_doc.tpl_dict, slides_mkdown.tpl_dict,

])
