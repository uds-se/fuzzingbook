#!/usr/bin/env python
"""html in standard nbconvert format
"""

from ipypublish.html.create_tpl import create_tpl
from ipypublish.html.standard import content
from ipypublish.html.standard import content_tagging
from ipypublish.html.standard import document
from ipypublish.html.standard import inout_prompt
from ipypublish.html.standard import mathjax
from ipypublish.html.standard import widgets

oformat = 'HTML'
config = {}
template = create_tpl([
    document.tpl_dict,
    content.tpl_dict, content_tagging.tpl_dict,
    mathjax.tpl_dict, widgets.tpl_dict,
    inout_prompt.tpl_dict
])
