#!/usr/bin/env python

"""
create template

philosophy is only turn stuff on when we want

http://nbconvert.readthedocs.io/en/latest/customizing.html#Template-structure
http://nbconvert.readthedocs.io/en/latest/api/exporters.html#nbconvert.exporters.TemplateExporter

"""
import logging

# % filter_data_type returns the first available format in the data priority
# ((* block execute_result scoped *))
#     ((*- for type in output.data | filter_data_type -*))
#         {notebook_output}
#     ((*- endfor -*))
# ((* endblock execute_result *))

TPLX_OUTLINE = r"""
((=
A latex document
{meta_docstring}
=))

((*- extends 'display_priority.tplx' -*))

%% Latex Document Setup
%% ====================

((* block header *))

	((*- block docclass *))
		{document_docclass}
	((* endblock docclass -*))

	((*- block packages *))
		{document_packages}
	((* endblock packages *))

	((*- block definitions *))
    	((* block date *))((* endblock date *))
    	((* block author *))((* endblock author *))
		((* block title *))((* endblock title *))

		{document_definitions}

	((* endblock definitions *))

	((*- block commands *))
		((* block margins *))
			{document_margins}
		((* endblock margins *))
		{document_commands}
	((* endblock commands *))

    {document_header_end}

((* endblock header *))

((* block body *))

	\begin{{document}}

	((* block predoc *))
		((* block maketitle *))
			{document_title}
		((* endblock maketitle *))
		((* block abstract *))
			{document_abstract}
		((* endblock abstract *))
		{document_predoc}
	((* endblock predoc *))

	((( super() )))

	((* block postdoc *))
    	((* block bibliography *))
			{document_bibliography}
		((* endblock bibliography *))
		{document_postdoc}
    ((* endblock postdoc *))

	\end{{document}}

((* endblock body *))

%% Notebook Input
%% ==============

((*- block any_cell scoped *))
	{notebook_input}
((* endblock any_cell *))

((* block input scoped *))
	{notebook_input_code}
((* endblock input *))

((* block rawcell scoped *))
	{notebook_input_raw}
((* endblock rawcell *))

((* block markdowncell scoped *))
	{notebook_input_markdown}
((* endblock markdowncell *))

((* block unknowncell scoped *))
	{notebook_input_unknown}
((* endblock unknowncell *))

%% Notebook Outbook
%% ================

% Redirect execute_result to display data priority.
((*- block execute_result scoped *))
    ((* block data_priority scoped *))
		{notebook_output}
    ((* endblock *))
((* endblock execute_result *))

((* block data_text *))
	{notebook_output_text}
((* endblock data_text *))

((* block error *))
	{notebook_output_error}
((* endblock error *))

((* block traceback_line *))
    {notebook_output_traceback}
((* endblock traceback_line *))

((* block stream *))
    {notebook_output_stream}
((* endblock stream *))

((* block data_latex -*))
	{notebook_output_latex}
((* endblock data_latex *))

((*- block data_markdown -*))
	{notebook_output_markdown}
((* endblock data_markdown *))

((*- block data_png -*))
	{notebook_output_png}
((*- endblock data_png -*))

((*- block data_jpg -*))
	{notebook_output_jpg}
((*- endblock data_jpg -*))

((*- block data_svg -*))
	{notebook_output_svg}
((*- endblock data_svg -*))

((*- block data_pdf -*))
	{notebook_output_pdf}
((*- endblock -*))


%% Jinja Macros
%% ================

{jinja_macros}
"""


def create_tplx(tplx_dicts=(), outpath=None):
    """ build a latex jinja template from multiple dictionaries,
    specifying fragments of the template to insert a specific points

    if a tplx_dict contains the key "overwrite",
    then its value should be a list of keys,
    such that these key values overwrite any entries before

    Parameters
    ----------
    tplx_dicts: list of dicts
    outpath: str
        if not None, output template to file

    """
    outline = TPLX_OUTLINE
    tplx_sections = {
        'meta_docstring': '',

        'document_docclass': '',
        'document_packages': '',
        'document_definitions': '',

        'document_margins': '',
        'document_commands': '',
        'document_header_end': '',

        'document_title': '',
        'document_abstract': '',
        'document_predoc': '',

        'document_bibliography': '',
        'document_postdoc': '',

        'notebook_input': '',
        'notebook_input_code': '',
        'notebook_input_raw': '',
        'notebook_input_markdown': '',
        'notebook_input_unknown': '',

        'notebook_output': '',
        'notebook_output_text': '',
        'notebook_output_error': '',
        'notebook_output_traceback': '',
        'notebook_output_stream': '',
        'notebook_output_latex': '',
        'notebook_output_markdown': '',
        'notebook_output_png': '',
        'notebook_output_jpg': '',
        'notebook_output_svg': '',
        'notebook_output_pdf': '',

        'jinja_macros': ''}

    for i, tplx_dict in enumerate(tplx_dicts):
        if 'overwrite' in list(tplx_dict.keys()):
            overwrite = tplx_dict['overwrite']
        else:
            overwrite = []
        logging.debug('overwrite keys: {}'.format(overwrite))
        for key, val in tplx_dict.items():
            if key == 'overwrite':
                pass
            elif key not in tplx_sections:
                raise ValueError(
                    '{0} from tplx_dict {1} not in outline tplx section'.format(key, i))
            elif key in overwrite:
                tplx_sections[key] = val
            else:
                tplx_sections[key] = tplx_sections[key] + '\n' + val

    outline = outline.format(**tplx_sections)

    if outpath is not None:
        with open(outpath, 'w') as f:
            f.write(outline)
        return
    return outline
