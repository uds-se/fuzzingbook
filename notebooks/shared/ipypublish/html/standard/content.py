#!/usr/bin/env python

tpl_dict = {

    'meta_docstring': 'with standard nbconvert input/output content',

    'notebook_all': r"""
  {{ super() }}
""",

    'notebook_input_markdown': r"""
{{ cell.source  | markdown2html | strip_files_prefix }}
""",

    'notebook_input_code': r"""
<div class="inner_cell">
<div class="input_area">
{{ cell.source | highlight_code(metadata=cell.metadata) }}
</div>
</div>
""",

    'notebook_input_unknown': r"""
unknown type  {{ cell.type }}
""",

    'notebook_output': r"""
 {{ super() }}
""",

    'notebook_output_error': r"""
 {{- super() -}}
""",

    'notebook_output_traceback': r"""
{{ line | ansi2html }}
""",

    'notebook_output_stream_stderr': r"""
{{- output.text | ansi2html -}}
""",

    'notebook_output_stream_stdout': r"""
{{- output.text | ansi2html -}}
""",

    'notebook_output_text': r"""
{{- output.data['text/plain'] | ansi2html -}}
""",

    'notebook_output_latex': r"""
{{ output.data['text/latex'] }}
""",

    'notebook_output_markdown': r"""
{{ output.data['text/markdown'] | markdown2html }}
""",

    'notebook_output_png': r"""
{%- if 'image/png' in output.metadata.get('filenames', {}) %}
<img src="{{ output.metadata.filenames['image/png'] | posix_path }}"
{%- else %}
<img src="data:image/png;base64,{{ output.data['image/png'] }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/png') -%}
{%- if width is not none %}
width={{ width }}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/png') -%}
{%- if height is not none %}
height={{ height }}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/png') %}
class="unconfined"
{%- endif %}
>
""",

    'notebook_output_jpg': r"""
{%- if 'image/jpeg' in output.metadata.get('filenames', {}) %}
<img src="{{ output.metadata.filenames['image/jpeg'] | posix_path }}"
{%- else %}
<img src="data:image/jpeg;base64,{{ output.data['image/jpeg'] }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/jpeg') -%}
{%- if width is not none %}
width={{ width }}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/jpeg') -%}
{%- if height is not none %}
height={{ height }}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/jpeg') %}
class="unconfined"
{%- endif %}
>
""",

    'notebook_output_svg': r"""
{%- if output.svg_filename %}
<img src="{{ output.svg_filename | posix_path }}"
{%- else %}
{{ output.data['image/svg+xml'] }}
{%- endif %}
""",

    'notebook_output_html': r"""
{{ output.data['text/html'] }}
""",

    'notebook_output_widget_state': r"""
{{ output.data[datatype] | json_dumps }}
""",

    'notebook_output_widget_view': r"""
{{ output.data[datatype] | json_dumps }}
""",

}
