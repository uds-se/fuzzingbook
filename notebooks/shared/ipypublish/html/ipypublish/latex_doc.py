# .figure img {
#     margin: 0 auto;
#     display: block;
#     max-width: 100%;
# }
# .figure {
#     padding: 0.9em;
#     background: #fff;
#     margin: 0 auto 1em;
#     display:table;
# }
# figure figcaption {
#     text-align: left;
# }

# .ipycaption { display: block; float:left; margin-left: 0; }
# .ipyfigure { display: -ms-flex; display: -webkit-flex; display: flex;}
# .ipyfigure>div { flex:1; }
# .ipytable { display: -ms-flex; display: -webkit-flex; display: flex;}
# .ipytable>div { flex:1; }

tpl_dict = {

    'meta_docstring': """ caption and label elements according to ipub meta tags  """,
    'overwrite': ['notebook_output', 'notebook_all', 'notebook_input_markdown',
                  'notebook_input_code', 'notebook_input_code_pre', 'notebook_input_code_post',
                  'notebook_output_text', 'notebook_output_stream_stderr', 'notebook_output_stream_stdout'],
    "globals": r"""
{% set slidecolumn = [] %}"
{% set sliderow = {} %}"
""",

    "html_header": r"""

<!--[if IE lte 8]><script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->

<style type="text/css">
.ipyfigure { display: -ms-flex; display: -webkit-flex; display: flex;}
.ipyfigure>div { flex:1; }
.ipytable { display: -ms-flex; display: -webkit-flex; display: flex;}
.ipytable>div { flex:1; }

</style>
""",

    "html_body_start": r"""
{%- if nb.metadata.ipub -%}
{%- if nb.metadata.ipub.titlepage -%}
<section>
{%- if nb.metadata.ipub.titlepage.title -%}
<h1>{{ nb.metadata.ipub.titlepage.title }}</h1>
{%- endif -%}
{%- if nb.metadata.ipub.titlepage.subtitle -%}
<h3>{{ nb.metadata.ipub.titlepage.subtitle }}</h3>
{%- endif -%}
{%- if nb.metadata.ipub.titlepage.author -%}
<b>by {{ nb.metadata.ipub.titlepage.author }}</b>
{%- endif -%}
</section>
{%- endif -%}
{%- endif -%}
""",

    'notebook_all': r"""
{%- if cell.metadata.ipub: -%}
    {%- if cell.metadata.ipub.ignore: -%}
    {%- elif cell.metadata.ipub.slideonly: -%}
    {%- else -%}
{{ super() }}
    {%- endif %}
{%- else -%}
{{ super() }}
{%- endif %}
""",

    'notebook_input_code_pre': r"""
{%- if cell.metadata.ipub: -%}
{%- if cell.metadata.ipub.code: -%}
{%- if cell.metadata.ipub.code.caption: -%}
<br>{{cell.metadata.ipub.code.caption | replace_string("{id_home_prefix}","#")}}
{%- endif %}
<div class="input_code">
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
{%- endif %}
{%- endif %}
""",
    'notebook_input_code': r"""
{%- if cell.metadata.ipub: -%}
{%- if cell.metadata.ipub.code: -%}
<div class="inner_cell">
<div class="input_area">
{%- if cell.metadata.ipub.code.label: -%}
<a id="{{cell.metadata.ipub.code.label}}" class="anchor-link" name="#{{cell.metadata.ipub.code.label}}"></a>
{% if resources.refslide.setdefault(cell.metadata.ipub.code.label,
            (slidecolumn | length - 1,sliderow.get('len',[]) | length)) %}{% endif %}
{%- endif %}
{{ cell.source | highlight_code(metadata=cell.metadata) }}
</div>
</div>
{%- endif %}
{%- endif %}
""",
    'notebook_input_code_post': r"""
{%- if cell.metadata.ipub: -%}
{%- if cell.metadata.ipub.code: -%}
</div>
</div>
</div>
{%- endif %}
{%- endif %}
""",

    'notebook_input_markdown': r"""
{{ cell.source  | markdown2html | strip_files_prefix | replace_string("{id_home_prefix}","#") }}
""",

    'notebook_output': r"""
{%- if cell.metadata.ipub: -%}
    {%- if cell.metadata.ipub.figure: -%}
{{ super() }}
    {%- elif cell.metadata.ipub.table: -%}
{{ super() }}
    {%- elif cell.metadata.ipub.equation: -%}
{{ super() }}
    {%- elif cell.metadata.ipub.text: -%}
{{ super() }}
    {%- elif cell.metadata.ipub.error: -%}
{{ super() }}
    {%- elif cell.metadata.ipub.mkdown: -%}
{{ super() }}
    {%- endif %}
{%- else -%}

{%- endif %}
""",

    'notebook_output_text': r"""
{%- if cell.metadata.ipub: -%}
    {%- if cell.metadata.ipub.text: -%}
{{- output.data['text/plain'] | ansi2html -}}
    {%- endif %}
{%- endif %}
""",

    'notebook_output_stream_stderr': r"""
{%- if cell.metadata.ipub: -%}
    {%- if cell.metadata.ipub.text: -%}
{{- output.text | ansi2html -}}
    {%- endif %}
{%- endif %}
""",

    'notebook_output_stream_stdout': r"""
{%- if cell.metadata.ipub: -%}
    {%- if cell.metadata.ipub.text: -%}
{{- output.text | ansi2html -}}
    {%- endif %}
{%- endif %}
""",

    'notebook_output_pre': r"""
{{ table_caption(cell.metadata) }}
""",
    'notebook_output_post': r"""
{{ figure_caption(cell.metadata) }}
""",

    'notebook_output_latex_pre': r"""
{{ make_figure_pre(cell.metadata) }}
{{ make_table_pre(cell.metadata) }}
{{ make_equation_pre(cell.metadata) }}
""",
    'notebook_output_latex_post': r"""
{{ make_figure_post(cell.metadata) }}
{{ make_table_post(cell.metadata) }}
{{ make_equation_post(cell.metadata) }}
""",

    'notebook_output_png_pre': r"""
{{ make_figure_pre(cell.metadata) }}
{{ make_table_pre(cell.metadata) }}
{{ make_equation_pre(cell.metadata) }}
""",
    'notebook_output_png_post': r"""
{{ make_figure_post(cell.metadata) }}
{{ make_table_post(cell.metadata) }}
{{ make_equation_post(cell.metadata) }}
""",

    'notebook_output_jpg_pre': r"""
{{ make_figure_pre(cell.metadata) }}
{{ make_table_pre(cell.metadata) }}
{{ make_equation_pre(cell.metadata) }}
""",
    'notebook_output_jpg_post': r"""
{{ make_figure_post(cell.metadata) }}
{{ make_table_post(cell.metadata) }}
{{ make_equation_post(cell.metadata) }}
""",

    'notebook_output_svg_pre': r"""
{{ make_figure_pre(cell.metadata) }}
{{ make_table_pre(cell.metadata) }}
{{ make_equation_pre(cell.metadata) }}
""",
    'notebook_output_svg_post': r"""
{{ make_figure_post(cell.metadata) }}
{{ make_table_post(cell.metadata) }}
{{ make_equation_post(cell.metadata) }}
""",

    'notebook_output_pdf_pre': r"""
{{ make_figure_pre(cell.metadata) }}
{{ make_table_pre(cell.metadata) }}
{{ make_equation_pre(cell.metadata) }}
""",
    'notebook_output_pdf_post': r"""
{{ make_figure_post(cell.metadata) }}
{{ make_table_post(cell.metadata) }}
{{ make_equation_post(cell.metadata) }}
""",

    'notebook_output_html_pre': r"""
{{ make_figure_pre(cell.metadata) }}
{{ make_table_pre(cell.metadata) }}
{{ make_equation_pre(cell.metadata) }}
""",
    'notebook_output_html_post': r"""
{{ make_figure_post(cell.metadata) }}
{{ make_table_post(cell.metadata) }}
{{ make_equation_post(cell.metadata) }}
""",

    'jinja_macros': r"""

{% macro make_figure_pre(meta) -%}
{%- if meta.ipub: -%}
    {%- if meta.ipub.figure: -%}

    {%- if meta.ipub.figure.label: -%}
<a id="{{meta.ipub.figure.label}}" class="anchor-link" name="#{{meta.ipub.figure.label}}"></a>
    {% if resources.refslide.setdefault(meta.ipub.figure.label,
        (slidecolumn | length - 1,sliderow.get('len',[]) | length)) %}{% endif %}
    {%- endif %}
    {%- endif %}
{%- endif %}
{%- endmacro %}

{% macro make_figure_post(meta) -%}
{%- if meta.ipub: -%}
    {%- if meta.ipub.figure: -%}

    {%- endif %}
{%- endif %}
{%- endmacro %}

{% macro figure_caption(meta) -%}
{%- if meta.ipub: -%}
{%- if meta.ipub.figure: -%}
{%- if meta.ipub.figure.caption: -%}
<div class="output_area">
<div class="cell border-box-sizing text_cell rendered">
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
{{meta.ipub.figure.caption | replace_string("{id_home_prefix}","#")}}
</div>
</div>
</div>
</div>
{%- endif %}
{%- endif %}
{%- endif %}
{%- endmacro %}

{% macro make_table_pre(meta) -%}
{%- if meta.ipub: -%}
    {%- if meta.ipub.table: -%}

        {%- if meta.ipub.table.label: -%}
<a id="{{meta.ipub.table.label}}" class="anchor-link" name="#{{meta.ipub.table.label}}"></a>
           {% if resources.refslide.setdefault(meta.ipub.table.label,
               (slidecolumn | length - 1,sliderow.get('len',[]) | length)) %}{% endif %}
        {%- endif %}
    {%- endif %}

{%- endif %}
{%- endmacro %}

{% macro make_table_post(meta) -%}
{%- if meta.ipub: -%}
    {%- if meta.ipub.table: -%}

    {%- endif %}
{%- endif %}
{%- endmacro %}

{% macro make_equation_pre(meta) -%}
{%- if meta.ipub: -%}
    {%- if meta.ipub.equation: -%}
    {%- endif %}
{%- endif %}
{%- endmacro %}

{% macro make_equation_post(meta) -%}
{%- if meta.ipub: -%}
    {%- if meta.ipub.equation: -%}
        {%- if meta.ipub.equation.label: -%}
<a id="{{meta.ipub.equation.label}}" class="anchor-link" name="#{{meta.ipub.equation.label}}"></a>
           {% if resources.refslide.setdefault(meta.ipub.equation.label,
               (slidecolumn | length - 1,sliderow.get('len',[]) | length)) %}{% endif %}
        {%- endif %}
    {%- endif %}
{%- endif %}
{%- endmacro %}

{% macro table_caption(meta) -%}
{%- if meta.ipub: -%}
{%- if meta.ipub.table: -%}
{%- if meta.ipub.table.caption: -%}
<div class="output_area">
<div class="cell border-box-sizing text_cell rendered">
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
{{meta.ipub.table.caption | replace_string("{id_home_prefix}","#")}}
</div>
</div>
</div>
</div>
{%- endif %}
{%- endif %}
{%- endif %}
{%- endmacro %}

""",

}
