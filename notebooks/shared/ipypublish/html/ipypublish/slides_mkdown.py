tpl_dict = {

    'meta_docstring': """sets markdown main titles (with one #) as their own slides,
remove code cells """,

    "overwrite": ['notebook_all',
                  'notebook_input_markdown'],

    "globals": r"""
{% set slidecolumn = [] %}"
{% set sliderow = {} %}"
""",

    # don't use slide meta tags at present
    'notebook_all': '{{ super() }}',
    # new slide on header, and sub-header
    'notebook_input_markdown_pre': r"""
{%- if cell.source[0] == '#' -%}
    {%- if cell.source[1] == '#' -%}
        {%- if cell.source[2] == '#' -%}

        {%- else -%}
            {% if slidecolumn | length != 0 %}
</section>
<section>
            {%- endif -%}
            {% if slidecolumn.append('1') %}{% endif %}
        {%- endif -%}
    {%- else -%}
            {% if slidecolumn | length != 0 %}
</section>
<section>
            {%- endif -%}
           {% if slidecolumn.append('1') %}{% endif %}
    {%- endif -%}
{%- endif -%}
""",

    'notebook_input_markdown': r"""
{{ cell.source  | markdown2html | strip_files_prefix }}
""",

}
