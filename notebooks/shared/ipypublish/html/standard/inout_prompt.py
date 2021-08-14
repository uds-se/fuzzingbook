#!/usr/bin/env python

tpl_dict = {

    'meta_docstring': 'with standard nbconvert input/output prompts',

    'notebook_input_code_prompt': r"""
<div class="prompt input_prompt">
{%- if cell.execution_count is defined -%}
{%- if resources.global_content_filter.include_input_prompt-%}
In&nbsp;[{{ cell.execution_count|replace(None, "&nbsp;") }}]:
{%- else -%}
In&nbsp;[&nbsp;]:
{%- endif -%}
{%- endif -%}
</div>
""",

    'notebook_output_prompt': r"""
{% if resources.global_content_filter.include_output_prompt %}
{% block output_area_prompt %}
{%- if output.output_type == 'execute_result' -%}
    <div class="prompt output_prompt">
{%- if cell.execution_count is defined -%}
    Out[{{ cell.execution_count|replace(None, "&nbsp;") }}]:
{%- else -%}
    Out[&nbsp;]:
{%- endif -%}
{%- else -%}
    <div class="prompt">
{%- endif -%}
    </div>
{% endblock output_area_prompt %}
{% endif %}
"""
}
