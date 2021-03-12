#!/usr/bin/env python

tplx_dict = {
    'overwrite': ['notebook_output', 'notebook_input_code'],
    'meta_docstring': 'with in/out prompts',
    'document_definitions': """

    % Exact colors from NB
    \definecolor{incolor}{rgb}{0.0, 0.0, 0.5}
    \definecolor{outcolor}{rgb}{0.545, 0.0, 0.0}

""",
    'notebook_input_code': """
    ((( add_prompt(cell.source | highlight_code(strip_verbatim=True, metadata=cell.metadata), cell, 'In ', 'incolor') )))

""",
    'notebook_output': r"""
        ((*- if resources.global_content_filter.include_output_prompt -*))
            ((*- if type in ['text/plain'] *))
((( add_prompt(output.data['text/plain'] | escape_latex, cell, 'Out', 'outcolor') )))
            ((* else -*))
\texttt{\color{outcolor}Out[{\color{outcolor}((( cell.execution_count )))}]:}((( super() )))
            ((*- endif -*))
        ((*- endif -*))

""",
    'jinja_macros': r"""
% Purpose: Renders an output/input prompt
((* macro add_prompt(text, cell, prompt, prompt_color) -*))
    ((*- if cell.execution_count is defined -*))
    ((*- set execution_count = "" ~ (cell.execution_count | replace(None, " ")) -*))
    ((*- else -*))
    ((*- set execution_count = " " -*))
    ((*- endif -*))
    ((*- set indention =  " " * (execution_count | length + 7) -*))
\begin{Verbatim}[commandchars=\\\{\}]
((( text | add_prompts(first='{\color{' ~ prompt_color ~ '}' ~ prompt ~ '[{\\color{' ~ prompt_color ~ '}' ~ execution_count ~ '}]:} ', cont=indention) )))
\end{Verbatim}
((*- endmacro *))

"""
}
