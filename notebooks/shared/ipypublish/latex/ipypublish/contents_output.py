tplx_dict = {
    'meta_docstring': 'with the main ipypublish content',

    'document_packages': r"""
((*- if nb.metadata.ipub: -*))
((*- if nb.metadata.ipub.enable_breqn: -*))
\usepackage{breqn}
((*- endif *))
((*- endif *))
""",

    'notebook_input': r"""
((*- if cell.metadata.ipub: -*))
    ((*- if cell.metadata.ipub.ignore: -*))
    ((*- elif cell.metadata.ipub.slideonly: -*))
    ((*- else -*))
    ((( super() )))
    ((*- endif *))
((*- else -*))
    ((( super() )))
((*- endif *))
""",

    'notebook_input_markdown': r"""
((( cell.source | citation2latex | strip_files_prefix | convert_pandoc('markdown', 'json',extra_args=[]) | resolve_references | convert_pandoc('json','latex'))))
""",

    'notebook_output': r"""
((*- if cell.metadata.ipub: -*))
    ((*- if cell.metadata.ipub.ignore: -*))
    ((*- elif cell.metadata.ipub.slideonly: -*))
    ((*- else -*))
    ((( super() )))
    ((*- endif *))
((*- else -*))
    ((( super() )))
((*- endif *))
""",

    'notebook_output_markdown': """
((*- if cell.metadata.ipub: -*))
    ((*- if cell.metadata.ipub.mkdown: -*))
((( output.data['text/markdown'] | citation2latex | strip_files_prefix | convert_pandoc('markdown', 'json',extra_args=[]) | resolve_references | convert_pandoc('json','latex'))))
((*- endif *))
((*- endif *))
""",

    'notebook_output_stream': r"""
((*- if cell.metadata.ipub: -*))
    ((*- if cell.metadata.ipub.ignore: -*))
    ((*- else -*))
    ((( super() )))
    ((*- endif *))
((*- else -*))
    ((( super() )))
((*- endif *))
""",

    'notebook_output_latex': r"""
((*- if cell.metadata.ipub: -*))

    ((*- if cell.metadata.ipub.table and cell.metadata.ipub.equation -*))

        ((*- if output.data['text/latex'] | is_equation -*))

            ((( draw_equation(cell.metadata, output.data['text/latex']) )))

        ((*- else -*))

            ((( draw_table(cell, resources, output.data['text/latex']) )))

        ((*- endif *))

    ((*- else -*))

    ((*- if cell.metadata.ipub.table: -*))

        ((( draw_table(cell, resources, output.data['text/latex']) )))

    ((*- elif cell.metadata.ipub.equation: -*))

        ((( draw_equation(cell.metadata, output.data['text/latex']) )))

    ((*- endif *))

    ((*- endif *))
((*- endif *))
""",

    # 'notebook_output_markdown':'',
    'notebook_output_png': r"""
((( draw_figure(output.metadata.filenames['image/png'],
cell.metadata) )))

""",
    'notebook_output_jpg': r"""
((( draw_figure(output.metadata.filenames['image/jpeg'],
cell.metadata) )))

""",
    'notebook_output_svg': r"""
((( draw_figure(output.metadata.filenames['image/svg+xml'],
cell.metadata) )))

""",
    'notebook_output_pdf': r"""
((( draw_figure(output.metadata.filenames['application/pdf'],
cell.metadata) )))

""",

    'jinja_macros': r"""
((* macro draw_figure(filename, meta) -*))
((*- if meta.ipub: -*))
((*- if meta.ipub.figure: -*))
((* set filename = filename | posix_path *))
((*- block figure scoped -*))

    ((*- if meta.ipub.figure.placement: -*))
        ((*- if meta.ipub.figure.widefigure: -*))
    \begin{figure*}[(((meta.ipub.figure.placement)))]
        ((*- else -*))
    \begin{figure}[(((meta.ipub.figure.placement)))]
        ((*- endif *))
    ((*- else -*))
        ((*- if meta.ipub.figure.widefigure: -*))
    \begin{figure*}
        ((*- else -*))
    \begin{figure}
        ((*- endif *))
    ((*- endif *))
        ((*- if meta.ipub.figure.width: -*))
        \begin{center}\adjustimage{max size={0.9\linewidth}{0.9\paperheight},width=(((meta.ipub.figure.width)))\linewidth}{((( filename )))}\end{center}
        ((*- elif meta.ipub.figure.height: -*))
        \begin{center}\adjustimage{max size={0.9\linewidth}{0.9\paperheight},height=(((meta.ipub.figure.height)))\paperheight}{((( filename )))}\end{center}
        ((*- else -*))
        \begin{center}\adjustimage{max size={0.9\linewidth}{0.9\paperheight}}{((( filename )))}\end{center}
        ((*- endif *))

        ((*- if resources.captions: -*))
            ((*- if resources.captions[meta.ipub.figure.label]: -*))
             \caption{((( resources.captions[meta.ipub.figure.label] )))}
            ((*- else -*))
             \caption{((( meta.ipub.figure.caption )))}
            ((*- endif *))
        ((*- elif meta.ipub.figure.caption: -*))
             \caption{((( meta.ipub.figure.caption )))}
        ((*- endif *))
        ((*- if meta.ipub.figure.label: -*))
        \label{((( meta.ipub.figure.label )))}
        ((*- endif *))
    \end{figure}

((*- endblock figure -*))
((*- endif *))
((*- endif *))
((*- endmacro *))

((* macro draw_table(cell, resources, text) -*))
((*- block table scoped -*))

((*- if cell.metadata.ipub.table.placement: -*))
\begin{table}[(((cell.metadata.ipub.table.placement)))]
((*- else -*))
\begin{table}
((*- endif *))

((*- if resources.captions and cell.metadata.ipub.table.label -*))
    ((*- if resources.captions[cell.metadata.ipub.table.label]: -*))
     \caption{((( resources.captions[cell.metadata.ipub.table.label] )))}
    ((*- elif cell.metadata.ipub.table.caption -*))
     \caption{((( cell.metadata.ipub.table.caption )))}
    ((*- endif *))
((*- elif cell.metadata.ipub.table.caption -*))
 \caption{((( cell.metadata.ipub.table.caption )))}
((*- endif *))

((*- if cell.metadata.ipub.table.label -*))
\label{((( cell.metadata.ipub.table.label )))}
((*- endif *))

\centering
\begin{adjustbox}{max width=\textwidth}
((*- if cell.metadata.ipub.table.alternate: -*))
\rowcolors{2}{(((cell.metadata.ipub.table.alternate)))}{white}
((*- endif *))
((( text )))
\end{adjustbox}
\end{table}

((*- endblock table -*))
((*- endmacro *))

((* macro draw_equation(meta, text) -*))
((*- block equation scoped -*))

((* set environment = "none" *))
((*- if meta.ipub.equation.environment: -*))
    ((*- if meta.ipub.equation.environment == "none" -*))
        ((* set environment = "none" *))
    ((*- elif meta.ipub.equation.environment == "equation" -*))
        ((* set environment = "equation" *))
    ((*- elif meta.ipub.equation.environment == "equation*" -*))
        ((* set environment = "equation*" *))
    ((*- elif meta.ipub.equation.environment == "align" -*))
        ((* set environment = "align" *))
    ((*- elif meta.ipub.equation.environment == "align*" -*))
        ((* set environment = "align*" *))
    ((*- elif meta.ipub.equation.environment == "multline" -*))
        ((* set environment = "multline" *))
    ((*- elif meta.ipub.equation.environment == "multline*" -*))
        ((* set environment = "multline*" *))
    ((*- elif meta.ipub.equation.environment == "breqn" -*))
        ((*- if nb.metadata.ipub: -*))
        ((*- if nb.metadata.ipub.enable_breqn: -*))
         ((* set environment = "dmath" *))
        ((*- endif *))
        ((*- endif *))
    ((*- elif meta.ipub.equation.environment == "breqn*" -*))
        ((*- if nb.metadata.ipub: -*))
        ((*- if nb.metadata.ipub.enable_breqn: -*))
         ((* set environment = "dmath*" *))
        ((*- endif *))
        ((*- endif *))
    ((*- elif meta.ipub.equation.environment == "gather" -*))
        ((* set environment = "gather" *))
    ((*- elif meta.ipub.equation.environment == "gather*" -*))
        ((* set environment = "gather*" *))
    ((*- endif *))
((*- endif *))

((* if environment == "none" *))

((( text )))

((*- else -*))

((*- if meta.ipub.equation.label and not "*" in environment -*))
\begin{(((environment)))}\label{((( meta.ipub.equation.label )))}
((*- else -*))
\begin{(((environment)))}
((*- endif *))
((( text | remove_dollars )))
\end{(((environment)))}

((*- endif *))

((*- endblock equation -*))
((*- endmacro *))

"""

}
