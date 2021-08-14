"""latex article in the main ipypublish format, preprocessed with default metadata tags:
- all output/code/error is rendered
- a basic titlepage and table of contents and tables of figures/tables/code
"""
from ipypublish.filters.ansi_listings import ansi2listings
from ipypublish.filters.filters import remove_dollars, first_para, create_key, dict_to_kwds, is_equation
from ipypublish.latex.create_tplx import create_tplx
from ipypublish.latex.ipypublish import biblio_natbib as bib
from ipypublish.latex.ipypublish import contents_framed_code as code
from ipypublish.latex.ipypublish import contents_output as output
from ipypublish.latex.ipypublish import doc_article as doc
from ipypublish.latex.ipypublish import front_pages as title
from ipypublish.latex.standard import standard_definitions as defs
from ipypublish.latex.standard import standard_packages as package
from ipypublish.preprocessors.latex_doc_captions import LatexCaptions
from ipypublish.preprocessors.latex_doc_defaults import MetaDefaults
from ipypublish.preprocessors.latex_doc_links import LatexDocLinks
from ipypublish.preprocessors.split_outputs import SplitOutputs

oformat = 'Latex'
template = create_tplx([p.tplx_dict for p in
                        [package, defs, doc, title, bib, output, code]])

_filters = {'remove_dollars': remove_dollars,
            'first_para': first_para,
            'create_key': create_key,
            'dict_to_kwds': dict_to_kwds,
            'ansi2listings': ansi2listings,
            'is_equation': is_equation}

cell_defaults = {
    "ipub": {
        "figure": {
            "placement": "H"
        },
        "table": {
            "placement": "H"
        },
        "equation": {'environment': 'equation'},
        "text": True,
        "mkdown": True,
        "code": True,
        "error": True
    }
}

nb_defaults = {
    "ipub": {
        "titlepage": {},
        "toc": True,
        "listfigures": True,
        "listtables": True,
        "listcode": True,
    }
}

config = {'TemplateExporter.filters': _filters,
          'Exporter.filters': _filters,
          'Exporter.preprocessors': [MetaDefaults, SplitOutputs, LatexDocLinks, LatexCaptions],
          'SplitOutputs.split': True,
          'MetaDefaults.cell_defaults': cell_defaults,
          'MetaDefaults.nb_defaults': nb_defaults}
