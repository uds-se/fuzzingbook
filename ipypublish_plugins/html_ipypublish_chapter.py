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
    'meta_docstring': 'with fuzzingbook adaptations',
    
# Fonts for page and menu
# See https://designshack.net/articles/css/10-great-google-font-combinations-you-can-copy/
    'html_header': """
{# Fonts #}
<link href='https://fonts.googleapis.com/css?family=Fira+Mono:400,500,700|Patua+One|Source+Code+Pro|Open+Sans' rel='stylesheet' type='text/css'>

{# Icons #}
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">

{# Open Graph Tags #}
<meta property="og:url" content="__CHAPTER_HTML__" />
<meta property="og:type" content="article" />
<meta property="og:title" content="__PAGE_TITLE__" />
<meta property="og:description" content="__DESCRIPTION__" />
<meta property="og:image" content="__BOOKIMAGE__" />

{# Do not collect Twitter data #}
<meta name="twitter:dnt" content="on">

{# Favicons #}
<link rel="shortcut icon" href="favicon/favicon.ico" type="image/x-icon">
<link rel="apple-touch-icon" sizes="152x152" href="favicon/apple-touch-icon.png">
{# <link rel="mask-icon" href="favicon/safari-pinned-tab.svg" color="#B03A2E"> #}
<meta name="msapplication-TileColor" content="#B03A2E">
<meta name="msapplication-config" content="favicon/browserconfig.xml">
<meta name="theme-color" content="#ffffff">
<link rel="icon" type="image/png" sizes="32x32" href="favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon/favicon-16x16.png">
<link rel="manifest" href="favicon/site.webmanifest">

{# Be more mobile-friendly #}
{# https://nipunbatra.github.io/blog/2017/Jupyter-powered-blog.html #}
<meta name="viewport" content="width=device-width, initial-scale=1">
    """,

# HTML headers and footers are added later by post-html script
    'overwrite': ['html_body_start', 'html_body_end'],

    'html_body_start': r"""
    <script>
    var close_menus = function() {
        /* doesn't work yet - AZ
        console.log("Closing menus")
        var cssmenu = document.getElementById("cssmenu")
        var all_items = cssmenu.getElementsByTagName("li");
        var i;
        for (i = 0; i < all_items.length; i++) {
            item = all_items[i];
            // console.log("<li>: ")
            // console.log(item.innerHTML);
            var j;
            var all_ul = item.getElementsByTagName("ul");
            for (j = 0; j < all_ul.length; j++) {
                console.log("<ul>: ")
                console.log(all_ul[j].innerHTML);
                all_ul[j].style.display = "none";
            }
            var all_ol = item.getElementsByTagName("ol");
            for (j = 0; j < all_ol.length; j++) {
                console.log("<ol>: ")
                console.log(all_ol[j].innerHTML);
                all_ol[j].style.display = "none";
            }
        }
        */
    };

    $( document ).ready( close_menus );

    // Let navbar fade away when scrolling down
    var prevScrollpos = window.pageYOffset;
    window.onscroll = function() {
        var currentScrollPos = window.pageYOffset;
        if (currentScrollPos > 10 && currentScrollPos > prevScrollpos) {
            // Hide navbar
            var cssmenu = document.getElementById("cssmenu")
            cssmenu.style.opacity = 0;
            
            // When scrolling, also close all sub-menus
            close_menus();
        }
        else {
            // Make navbar visible
            document.getElementById("cssmenu").style.opacity = 1;
        }
        prevScrollpos = currentScrollPos;
    };
    </script>
    <__HEADER__>
    <article>
   <div tabindex="-1" id="notebook" class="border-box-sizing">
     <div class="container" id="notebook-container">
""" + latex_doc.tpl_dict['html_body_start'],

    'html_body_end': r"""
        <__FOOTER__>
      </div>
    </div>
    </article>
"""
}


def hide_solution(key, tpl_dict = latex_doc.tpl_dict):
    """Hide solutions by default"""

    return """
       {%- if cell.metadata.solution_first or cell.metadata.solution2_first or cell.solution_first or cell.solution2_first -%}
    {# exercise #}
       {%- elif cell.metadata.solution == 'hidden' or cell.metadata.solution2 == 'hidden' or cell.solution == 'hidden' or cell.solution2 == 'hidden' -%}
    {# solution #}
    <span class="solution" style="display: none;">
       {%- else -%}
    {# some other cell #}
       {%- endif -%}""" + tpl_dict[key] + """
       {%- if cell.metadata.solution_first or cell.metadata.solution2_first or cell.solution_first or cell.solution2_first -%}
    {# end of exercise #}
    <__END_OF_EXERCISE__>
       {%- elif cell.metadata.solution == 'hidden' or cell.metadata.solution2 == 'hidden' or cell.solution == 'hidden' or cell.solution2 == 'hidden' -%}
    {# end of solution #}
    </span>
       {%- else -%}
    {# some other cell #}
       {%- endif -%}
    """

solutions_tpl_dict = {
    'overwrite': ['notebook_input_markdown', 'notebook_input_code', 
                  'notebook_output', 'notebook_all'],
    
    # Hide solution cells and add some text to last exercise cell
    'notebook_input_markdown': hide_solution('notebook_input_markdown'),
    'notebook_input_code': hide_solution('notebook_input_code'),
    'notebook_output': hide_solution('notebook_output'),
    
    # Do not even produce solution cells
    'notebook_all': r"""
{%- if cell.metadata.solution == 'hidden' or cell.metadata.solution2 == 'hidden' or cell.solution == 'hidden' or cell.solution2 == 'hidden' -%}
{%- if cell.metadata.solution_first or cell.metadata.solution2_first or cell.solution_first or cell.solution2_first -%}
    {# exercise #}
    """ + latex_doc.tpl_dict['notebook_all'] + """
{%- else -%}
    {# solution - ignore #}
{%- endif -%}
{%- else -%}
    {# regular cell #}
    """ + latex_doc.tpl_dict['notebook_all'] + """
{%- endif -%}
    """,    
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
    fuzzingbook_tpl_dict,
    solutions_tpl_dict
])
