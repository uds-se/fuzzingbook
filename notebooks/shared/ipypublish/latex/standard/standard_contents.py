#!/usr/bin/env python

tplx_dict = {
    'meta_docstring': 'with standard nbconvert input/output content',

    'notebook_input': """
 ((( super() )))
""",

    'notebook_input_code': """
    ((( cell.source | highlight_code(strip_verbatim=True, metadata=cell.metadata) )))

""",

    'notebook_input_markdown': """
    ((( cell.source | citation2latex | strip_files_prefix | convert_pandoc('markdown', 'json',extra_args=[]) | resolve_references | convert_pandoc('json','latex'))))

""",

    'notebook_output': """
 ((( super() )))
""",

    'notebook_output_text': r"""
    \begin{verbatim}
((( output.data['text/plain'] )))
    \end{verbatim}
""",
    'notebook_output_error': r"""
    \begin{Verbatim}[commandchars=\\\{\}]
((( super() )))
    \end{Verbatim}
""",
    'notebook_output_traceback': """
((( line | indent | strip_ansi | escape_latex )))
""",
    'notebook_output_stream': r"""
    \begin{Verbatim}[commandchars=\\\{\}]
((( output.text | escape_latex | ansi2latex )))
    \end{Verbatim}
""",
    'notebook_output_latex': """
 ((( output.data['text/latex'] | strip_files_prefix )))
""",
    'notebook_output_markdown': """
((( output.data['text/markdown'] | citation2latex | strip_files_prefix | convert_pandoc('markdown', 'latex'))))
""",
    'notebook_output_png': """
((( draw_figure(output.metadata.filenames['image/png']) )))
""",
    'notebook_output_jpg': """
((( draw_figure(output.metadata.filenames['image/jpeg']) )))
""",
    'notebook_output_svg': """
((( draw_figure(output.metadata.filenames['image/svg+xml']) )))
""",
    'notebook_output_pdf': """
((( draw_figure(output.metadata.filenames['application/pdf']) )))
""",

    'jinja_macros': r"""
% Draw a figure using the graphicx package.
((* macro draw_figure(filename) -*))
((* set filename = filename | posix_path *))
((*- block figure scoped -*))
    \begin{center}
    \adjustimage{max size={0.9\linewidth}{0.9\paperheight}}{((( filename )))}
    \end{center}
    { \hspace*{\fill} \\}
((*- endblock figure -*))
((*- endmacro *))

"""
}
