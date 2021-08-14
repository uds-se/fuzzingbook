tpl_dict = {

    'meta_docstring': 'with jupyter wigets',

    'html_header': r"""

{%- if "widgets" in nb.metadata -%}
<script src="https://unpkg.com/jupyter-js-widgets@2.0.*/dist/embed.js"></script>
{%- endif-%}

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

""",

    'html_footer': r"""

{% set mimetype = 'application/vnd.jupyter.widget-state+json'%}
{% if mimetype in nb.metadata.get("widgets",{})%}
<script type="{{ mimetype }}">
{{ nb.metadata.widgets[mimetype] | json_dumps }}
</script>
{% endif %}

"""
}
