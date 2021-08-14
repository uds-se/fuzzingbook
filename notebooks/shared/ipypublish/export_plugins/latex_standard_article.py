"""latex article in the standard nbconvert format
"""

from ipypublish.latex.create_tplx import create_tplx
from ipypublish.latex.standard import in_out_prompts as prompts
from ipypublish.latex.standard import standard_article as doc
from ipypublish.latex.standard import standard_contents as content
from ipypublish.latex.standard import standard_definitions as defs
from ipypublish.latex.standard import standard_packages as package

oformat = 'Latex'
template = create_tplx(
    [package.tplx_dict, defs.tplx_dict, doc.tplx_dict,
     content.tplx_dict, prompts.tplx_dict])

config = {'TemplateExporter.filters': {},
          'Exporter.filters': {}}
