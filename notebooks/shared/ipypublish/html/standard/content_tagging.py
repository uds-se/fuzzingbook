tpl_dict = {

    'meta_docstring': 'standard html tag wrapping',

    'notebook_input_code_pre': r"""
<div class="input_code">
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
""",
    'notebook_input_code_post': r"""
</div>
</div>
</div>
""",

    'notebook_input_raw_pre': r"""
<div class="input_raw">
<div class="cell border-box-sizing text_cell rendered">
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
""",
    'notebook_input_raw_post': r"""
</div>
</div>
</div>
</div>
""",

    'notebook_input_markdown_pre': r"""
<div class="input_markdown">
<div class="cell border-box-sizing text_cell rendered">
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
""",
    'notebook_input_markdown_post': r"""
</div>
</div>
</div>
</div>
""",

    'notebook_input_unknown_pre': r"""
<div class="input_unknown">
""",
    'notebook_input_unknown_post': r"""
</div>
""",

    'notebook_output_pre': r"""
<div class="output_area">""",
    'notebook_output_post': r"""
</div>
""",

    'notebook_output_error_pre': r"""
<div class="output_subarea output_text output_error">
<pre>
""",
    'notebook_output_error_post': r"""
</pre>
</div>
""",

    'notebook_output_traceback_pre': r"""
 <div class="output_traceback">
""",
    'notebook_output_traceback_post': r"""
</div>
""",

    'notebook_output_text_pre': r"""
<div class="output_text output_subarea {{ extra_class }}">
<pre>
""",
    'notebook_output_text_post': r"""
</pre>
</div>
""",

    'notebook_output_latex_pre': r"""
<div class="output_latex output_subarea {{ extra_class }}">
""",
    'notebook_output_latex_post': r"""
</div>
""",

    'notebook_output_stream_stdout_pre': r"""
<div class="output_subarea output_stream output_stdout output_text">
<pre>
""",
    'notebook_output_stream_stdout_post': r"""
</pre>
</div>
""",

    'notebook_output_stream_stderr_pre': r"""
<div class="output_subarea output_stream output_stderr output_text">
<pre>
""",
    'notebook_output_stream_stderr_post': r"""
</pre>
</div>
""",

    'notebook_output_markdown_pre': r"""
<div class="output_markdown rendered_html output_subarea {{ extra_class }}">
""",
    'notebook_output_markdown_post': r"""
</div>
""",

    'notebook_output_jpg_pre': r"""
<div class="output_image output_jpeg output_subarea {{ extra_class }}">
""",
    'notebook_output_jpg_post': r"""
</div>
""",

    'notebook_output_png_pre': r"""
<div class="output_image output_png output_subarea {{ extra_class }}">
""",
    'notebook_output_png_post': r"""
</div>
""",

    'notebook_output_svg_pre': r"""
<div class="output_image output_svg output_subarea {{ extra_class }}">
""",
    'notebook_output_svg_post': r"""
</div>
""",

    'notebook_output_pdf_pre': r"""
<div class="output_pdf output_subarea {{ extra_class }}">
""",
    'notebook_output_pdf_post': r"""
</div>
""",

    'notebook_output_html_pre': r"""
<div class="output_html rendered_html output_subarea {{ extra_class }}">
""",
    'notebook_output_html_post': r"""
</div>
""",

    'notebook_output_javascript_pre': r"""
{% set div_id = uuid4() %}
<div id="{ div_id }"></div>
<div class="output_subarea output_javascript {{ extra_class }}">
<script type="text/javascript">
var element = $('#{ div_id }');
""",
    'notebook_output_javascript_post': r"""
</script>
</div>
""",

    'notebook_output_widget_state_pre': r"""
{% set div_id = uuid4() %}
{% set datatype_list = output.data | filter_data_type %}
{% set datatype = datatype_list[0]%}
<div id="{ div_id }"></div>
<div class="output_subarea output_widget_state {{ extra_class }}">
<script type="text/javascript">
var element = $('#{ div_id }');
</script>
<script type="{ datatype }">
""",
    'notebook_output_widget_state_post': r"""
</script>
</div>
""",

    'notebook_output_widget_view_pre': r"""
{% set div_id = uuid4() %}
{% set datatype_list = output.data | filter_data_type %}
{% set datatype = datatype_list[0]%}
<div id="{ div_id }"></div>
<div class="output_subarea output_widget_view {{ extra_class }}">
<script type="text/javascript">
var element = $('#{ div_id }');
</script>
<script type="{ datatype }">
""",
    'notebook_output_widget_view_post': r"""
</script>
</div>
""",

}
