#!/usr/bin/env python

"""
create template

philosophy is only turn stuff on when we want

http://nbconvert.readthedocs.io/en/latest/customizing.html#Template-structure
http://nbconvert.readthedocs.io/en/latest/api/exporters.html#nbconvert.exporters.TemplateExporter

"""
import logging

TPL_OUTLINE = r"""
<!-- A html document -->
<!-- {meta_docstring} -->


{{%- extends 'display_priority.tpl' -%}}

{globals}

%% HTML Setup
%% ====================

{{%- block header %}}
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
{{%- block html_head -%}}
    {html_header}
{{%- endblock html_head -%}}
</head>
{{%- endblock header -%}}

{{% block body %}}
 <body>
 {html_body_start}
 {{{{ super() }}}}
 {html_body_end}
 </body>
{{%- endblock body %}}

{{%- block footer %}}
    {html_footer}
</html>
{{%- endblock footer-%}}

%% Notebook Input
%% ==============

{{%- block any_cell scoped %}}
{notebook_all}
{{% endblock any_cell %}}

{{% block input_group -%}}
{notebook_input_code_pre}
{{{{ super() }}}}
{notebook_input_code_post}
{{% endblock input_group %}}

{{% block in_prompt -%}}
{notebook_input_code_prompt}
{{%- endblock in_prompt %}}

{{% block input scoped %}}
{notebook_input_code}
{{% endblock input %}}

{{% block rawcell scoped %}}
{notebook_input_raw_pre}
{notebook_input_raw}
{notebook_input_raw_post}
{{% endblock rawcell %}}

{{% block markdowncell scoped %}}
{notebook_input_markdown_pre}
{notebook_input_markdown}
{notebook_input_markdown_post}
{{% endblock markdowncell %}}

{{% block unknowncell scoped %}}
{notebook_input_unknown_pre}
{notebook_input_unknown}
{notebook_input_unknown_post}
{{% endblock unknowncell %}}

%% Notebook Outbook
%% ================

{{% block output %}}
{notebook_output_pre}
{notebook_output_prompt}
{{{{ super() }}}}
{notebook_output_post}
{{% endblock output %}}

% Redirect execute_result to display data priority.
{{%- block execute_result scoped %}}
    {{%- set extra_class="output_execute_result" -%}}
    {{% block data_priority scoped %}}
{notebook_output}
    {{% endblock %}}
    {{%- set extra_class="" -%}}
{{% endblock execute_result %}}

{{% block error %}}
{notebook_output_error_pre}
{notebook_output_error}
{notebook_output_error_post}
{{% endblock error %}}

{{% block traceback_line %}}
{notebook_output_traceback_pre}
{notebook_output_traceback}
{notebook_output_traceback_post}
{{% endblock traceback_line %}}

{{% block data_text %}}
{notebook_output_text_pre}
{notebook_output_text}
{notebook_output_text_post}
{{% endblock data_text %}}

{{% block data_latex %}}
{notebook_output_latex_pre}
{notebook_output_latex}
{notebook_output_latex_post}
{{% endblock data_latex %}}


{{% block stream_stdout %}}
{notebook_output_stream_stdout_pre}
{notebook_output_stream_stdout}
{notebook_output_stream_stdout_post}
{{% endblock stream_stdout %}}

{{% block stream_stderr %}}
{notebook_output_stream_stderr_pre}
{notebook_output_stream_stderr}
{notebook_output_stream_stderr_post}
{{% endblock stream_stderr %}}

{{%- block data_markdown -%}}
{notebook_output_markdown_pre}
{notebook_output_markdown}
{notebook_output_markdown_post}
{{% endblock data_markdown %}}

{{%- block data_jpg -%}}
{notebook_output_jpg_pre}
{notebook_output_jpg}
{notebook_output_jpg_post}
{{%- endblock data_jpg -%}}

{{%- block data_png -%}}
{notebook_output_png_pre}
{notebook_output_png}
{notebook_output_png_post}
{{%- endblock data_png -%}}

{{%- block data_svg -%}}
{notebook_output_svg_pre}
{notebook_output_svg}
{notebook_output_svg_post}
{{%- endblock data_svg -%}}

{{%- block data_pdf -%}}
{notebook_output_pdf_pre}
{notebook_output_pdf}
{notebook_output_pdf_post}
{{%- endblock -%}}

{{% block data_html -%}}
{notebook_output_html_pre}
{notebook_output_html}
{notebook_output_html_post}
{{% endblock data_html%}}

{{%- block data_javascript scoped %}}
{notebook_output_javascript_pre}
{notebook_output_javascript}
{notebook_output_javascript_post}
{{%- endblock -%}}

{{%- block data_widget_state scoped %}}
{notebook_output_widget_state_pre}
{notebook_output_widget_state}
{notebook_output_widget_state_post}
{{%- endblock data_widget_state -%}}

{{%- block data_widget_view scoped %}}
{notebook_output_widget_view_pre}
{notebook_output_widget_view}
{notebook_output_widget_view_post}
{{%- endblock data_widget_view -%}}

%% Jinja Macros
%% ================

{jinja_macros}
"""


def create_tpl(tpl_dicts=(), outpath=None):
    """ build an html jinja template from multiple dictionaries,
    specifying fragments of the template to insert a specific points

    if a tpl_dict contains the key "overwrite",
    then its value should be a list of keys,
    such that these key values overwrite any entries before

    Parameters
    ----------
    tpl_dicts: list of dicts
    outpath: str
        if not None, output template to file

    """
    outline = TPL_OUTLINE
    tpl_sections = {
        'meta_docstring': '',
        'globals': '',

        'html_header': '',
        'html_body_start': '',
        'html_body_end': '',
        'html_footer': '',

        'notebook_all': '',

        'notebook_input_code_prompt': '',
        'notebook_input_code': '',
        'notebook_input_raw': '',
        'notebook_input_markdown': '',
        'notebook_input_unknown': '',
        'notebook_input_code_pre': '',
        'notebook_input_raw_pre': '',
        'notebook_input_markdown_pre': '',
        'notebook_input_unknown_pre': '',
        'notebook_input_code_post': '',
        'notebook_input_raw_post': '',
        'notebook_input_markdown_post': '',
        'notebook_input_unknown_post': '',

        'notebook_output': '',
        'notebook_output_prompt': '',
        'notebook_output_text': '',
        'notebook_output_error': '',
        'notebook_output_traceback': '',
        'notebook_output_stream_stderr': '',
        'notebook_output_stream_stdout': '',
        'notebook_output_latex': '',
        'notebook_output_markdown': '',
        'notebook_output_png': '',
        'notebook_output_jpg': '',
        'notebook_output_svg': '',
        'notebook_output_pdf': '',
        'notebook_output_html': '',
        'notebook_output_javascript': '',
        'notebook_output_widget_state': '',
        'notebook_output_widget_view': '',

        'notebook_output_pre': '',
        'notebook_output_text_pre': '',
        'notebook_output_error_pre': '',
        'notebook_output_traceback_pre': '',
        'notebook_output_stream_stderr_pre': '',
        'notebook_output_stream_stdout_pre': '',
        'notebook_output_latex_pre': '',
        'notebook_output_markdown_pre': '',
        'notebook_output_png_pre': '',
        'notebook_output_jpg_pre': '',
        'notebook_output_svg_pre': '',
        'notebook_output_pdf_pre': '',
        'notebook_output_html_pre': '',
        'notebook_output_javascript_pre': '',
        'notebook_output_widget_state_pre': '',
        'notebook_output_widget_view_pre': '',

        'notebook_output_post': '',
        'notebook_output_text_post': '',
        'notebook_output_error_post': '',
        'notebook_output_traceback_post': '',
        'notebook_output_stream_stderr_post': '',
        'notebook_output_stream_stdout_post': '',
        'notebook_output_latex_post': '',
        'notebook_output_markdown_post': '',
        'notebook_output_png_post': '',
        'notebook_output_jpg_post': '',
        'notebook_output_svg_post': '',
        'notebook_output_pdf_post': '',
        'notebook_output_html_post': '',
        'notebook_output_javascript_post': '',
        'notebook_output_widget_state_post': '',
        'notebook_output_widget_view_post': '',

        'jinja_macros': ''}

    for i, tpl_dict in enumerate(tpl_dicts):
        if 'overwrite' in list(tpl_dict.keys()):
            overwrite = tpl_dict['overwrite']
        else:
            overwrite = []
        logging.debug('overwrite keys: {}'.format(overwrite))
        for key, val in tpl_dict.items():
            if key == 'overwrite':
                pass
            elif key not in tpl_sections:
                raise ValueError(
                    '{0} from tpl_dict {1} not in outline tpl section'.format(key, i + 1))
            elif key in overwrite:
                tpl_sections[key] = val
            # if its pre then add befor existing (if post add after)
            elif '_pre' in key:
                tpl_sections[key] = val + '\n' + tpl_sections[key]
            else:
                tpl_sections[key] = tpl_sections[key] + '\n' + val

    outline = outline.format(**tpl_sections)

    if outpath is not None:
        with open(outpath, 'w') as f:
            f.write(outline)
        return
    return outline
