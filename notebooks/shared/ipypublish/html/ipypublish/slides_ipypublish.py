tpl_dict = {

    'overwrite': ['notebook_all', 'html_body_start', 'notebook_input_markdown'],

    'meta_docstring': 'marks up html with slide tags, based on metadata',

    "globals": r"""
{% set slidecolumn = [] %}"
{% set sliderow = {'len':[]} %}"
""",

    'html_body_start': r"""
<div class="reveal">
<div class="slides">

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

{%- if cell.metadata.ipyslides == 'skip' -%}
{%- endif -%}

{%- if cell.metadata.ipyslides == 'notes' -%}
<aside class="notes">
{{ super() }}
</aside>
{%- endif -%}

{%- if cell.metadata.ipyslides == 'first_cell' -%}
{% if slidecolumn.append('1') %}{% endif %}
{% if sliderow.update({'len':[]}) %}{% endif %}
<section>
{{ super() }}
{%- endif -%}

{%- if cell.metadata.ipyslides == 'horizontalbreak_before' -%}
{{ super() }}
</section>
</section>
{%- endif -%}


{%- if cell.metadata.ipyslides == 'horizontalbreak_after_novertical' -%}
{% if slidecolumn.append('1') %}{% endif %}
{% if sliderow.update({'len':[]}) %}{% endif %}
<section>
{{ super() }}
</section>
{%- endif -%}

{%- if cell.metadata.ipyslides == 'horizontalbreak_after_plusvertical' -%}
{% if slidecolumn.append('1') %}{% endif %}
{% if sliderow.update({'len':[]}) %}{% endif %}
<section>
<section>
{{ super() }}
</section>
<section>
{%- endif -%}

{%- if cell.metadata.ipyslides == 'horizontalbreak_after' -%}
{% if slidecolumn.append('1') %}{% endif %}
{% if sliderow.update({'len':[]}) %}{% endif %}
<section>
<section>
{{ super() }}
{%- endif -%}


{%- if cell.metadata.ipyslides == 'normal' -%}
{{ super() }}
{%- endif -%}

{%- if cell.metadata.ipyslides == 'verticalbreak_after' -%}
{% if sliderow['len'].append('1') %}{% endif %}
</section>
<section>
{{ super() }}
{%- endif -%}

{%- if cell.metadata.ipyslides == 'last_cell' -%}
{{ super() }}
</section>
</section>
{%- endif -%}


""",

    'notebook_input_markdown': r"""
{{ cell.source  | markdown2html | strip_files_prefix }}
""",

}
