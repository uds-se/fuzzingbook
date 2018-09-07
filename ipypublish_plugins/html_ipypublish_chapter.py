r"""html in ipypublish format, preprocessed with default metadata tags
- a table of contents
- toggle buttons for showing/hiding code & output cells
- converts or removes (if no converter) latex tags (like \cite{abc}, \ref{})
- all code/errors/output is shown unless tagged otherwise
"""

from ipypublish.filters.replace_string import replace_string
from ipypublish.html.create_tpl import create_tpl
from ipypublish.html.ipypublish import latex_doc
# from ipypublish.html.standard import inout_prompt
from ipypublish.html.ipypublish import toc_sidebar
from ipypublish.html.ipypublish import toggle_buttons
from ipypublish.html.standard import content
from ipypublish.html.standard import content_tagging
from ipypublish.html.standard import document
from ipypublish.html.standard import mathjax
from ipypublish.html.standard import widgets
from ipypublish.preprocessors.latex_doc_captions import LatexCaptions
from ipypublish.preprocessors.latex_doc_defaults import MetaDefaults
from ipypublish.preprocessors.latex_doc_html import LatexDocHTML
from ipypublish.preprocessors.latex_doc_links import LatexDocLinks
from ipypublish.preprocessors.latextags_to_html import LatexTagsToHTML
from ipypublish.preprocessors.split_outputs import SplitOutputs

# Own adaptations -- AZ
fuzzingbook_tpl_dict = {
    'meta_docstring': 'with fuzzingbook css adaptations',
    
# Fonts for page and menu
# See https://designshack.net/articles/css/10-great-google-font-combinations-you-can-copy/
    'html_header': """
<!-- Load Google fonts -->
<link href='https://fonts.googleapis.com/css?family=Patua+One|Source+Code+Pro|Open+Sans' rel='stylesheet' type='text/css'>

<!-- Icon library -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
    """,

# HTML headers and footers are added later by post-html script
    'overwrite': ['html_body_start', 'html_body_end', 'notebook_input_code'],

    'html_body_start': r"""
    <__HEADER__>
    <article>
   <div tabindex="-1" id="notebook" class="border-box-sizing">
     <div class="container" id="notebook-container">
""",

    'html_body_end': r"""
        <__FOOTER__>
      </div>
    </div>
    </article>
""",

# Solutions
    'notebook_input_markdown_pre': r"""
   {%- if cell.metadata.solution_first or cell.metadata.solution2_first or cell.solution_first or cell_solution2_first -%}
   <!-- exercise -->
   {%- elif cell.metadata.solution == 'hidden' or cell.metadata.solution2 == 'hidden' or cell.solution == 'hidden' or cell.solution2 == 'hidden' -%}
   <!-- solution -->
   <div style="display: none;" class="solution">
   {%- endif -%}
""",

    'notebook_input_markdown_post': r"""
   {%- if cell.metadata.solution_first or cell.metadata.solution2_first or cell.solution_first or cell_solution2_first -%}
   <!-- end of exercise -->
   {%- elif cell.metadata.solution == 'hidden' or cell.metadata.solution2 == 'hidden' or cell.solution == 'hidden' or cell.solution2 == 'hidden' -%}
   <!-- end of solution -->
   </div>
   {%- endif -%}
""",

    'notebook_input_code': r"""
   {%- if cell.metadata.solution_first or cell.metadata.solution2_first or cell.solution_first or cell_solution2_first -%}
<!-- exercise -->
<div class="inner_cell">
   {%- elif cell.metadata.solution == 'hidden' or cell.metadata.solution2 == 'hidden' or cell.solution == 'hidden' or cell.solution2 == 'hidden' -%}
<!-- solution -->
<div class="inner_cell" style="display: none;">
   {%- else -%}
<div class="inner_cell">
   {%- endif -%}
<div class="input_area">
{{ cell.source | highlight_code(metadata=cell.metadata) }}
</div>
</div>
   {%- if cell.metadata.solution_first or cell.metadata.solution2_first or cell.solution_first or cell_solution2_first -%}
<!-- end of exercise -->
   {%- elif cell.metadata.solution == 'hidden' or cell.metadata.solution2 == 'hidden' or cell.solution == 'hidden' or cell.solution2 == 'hidden' -%}
<!-- end of solution -->
   {%- endif -%}
"""
}

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

oformat = 'HTML'
config = {'TemplateExporter.filters': {'replace_string': replace_string},
          'Exporter.filters': {'replace_string': replace_string},
          'Exporter.preprocessors': [MetaDefaults, SplitOutputs, LatexDocLinks, LatexDocHTML, LatexTagsToHTML,
                                     LatexCaptions],
          'SplitOutputs.split': True,
          'MetaDefaults.cell_defaults': cell_defaults,
          'MetaDefaults.nb_defaults': nb_defaults,
          'LatexCaptions.add_prefix': True}

template = create_tpl([
    document.tpl_dict,
    content.tpl_dict, content_tagging.tpl_dict,
    mathjax.tpl_dict, widgets.tpl_dict,
    # inout_prompt.tpl_dict,
    # toggle_buttons.tpl_dict, 
    # toc_sidebar.tpl_dict,
    latex_doc.tpl_dict,
    fuzzingbook_tpl_dict
])
