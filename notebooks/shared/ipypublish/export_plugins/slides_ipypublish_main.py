#!/usr/bin/env python
r"""revel.js slides in the ipypublish format;
- resolves or removes (if no converter) latex tags (like \cite{abc}, \ref{})
- splits notebook into slide rows/columns, based on markdown headers
"""

from ipypublish.filters.replace_string import replace_string
from ipypublish.html.create_tpl import create_tpl
from ipypublish.html.ipypublish import latex_doc
from ipypublish.html.ipypublish import slides_ipypublish
from ipypublish.html.standard import content
from ipypublish.html.standard import content_tagging
from ipypublish.html.standard import mathjax
from ipypublish.html.standard import slides
from ipypublish.html.standard import widgets
from ipypublish.preprocessors.latex_doc_captions import LatexCaptions
from ipypublish.preprocessors.latex_doc_html import LatexDocHTML
from ipypublish.preprocessors.latex_doc_links import LatexDocLinks
from ipypublish.preprocessors.latextags_to_html import LatexTagsToHTML
from ipypublish.preprocessors.slides_from_markdown import MarkdownSlides
from ipypublish.preprocessors.split_outputs import SplitOutputs

oformat = 'Slides'

_filters = {'replace_string': replace_string}

config = {'TemplateExporter.filters': _filters,
          'Exporter.filters': _filters,
          'Exporter.preprocessors': [SplitOutputs, LatexDocLinks, LatexDocHTML, LatexTagsToHTML,
                                     LatexCaptions, MarkdownSlides],
          'SplitOutputs.split': True,
          'MarkdownSlides.column_level': 1,
          'MarkdownSlides.row_level': 0,
          'MarkdownSlides.header_slide': False,
          'MarkdownSlides.max_cells': 0,
          'MarkdownSlides.autonumbering': True,
          'LatexDocHTML.src_name': "data-src",
          'LatexCaptions.add_prefix': True}

template = create_tpl([
    content.tpl_dict, content_tagging.tpl_dict,
    mathjax.tpl_dict, widgets.tpl_dict,
    slides.tpl_dict, latex_doc.tpl_dict, slides_ipypublish.tpl_dict,

])
