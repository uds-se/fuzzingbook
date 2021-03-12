tplx_dict = {
    'meta_docstring': 'with the input code wrapped and framed',

    'document_packages': r"""

    % define a code float
    \usepackage{newfloat} % to define a new float types
    \DeclareFloatingEnvironment[
        fileext=frm,placement={!ht},
        within=section,name=Code]{codecell}
    \DeclareFloatingEnvironment[
        fileext=frm,placement={!ht},
        within=section,name=Text]{textcell}
    \DeclareFloatingEnvironment[
        fileext=frm,placement={!ht},
        within=section,name=Text]{errorcell}

    \usepackage{listings} % a package for wrapping code in a box
    \usepackage[framemethod=tikz]{mdframed} % to fram code

""",

    'document_header_end': r"""
% make the code float work with cleverref
\crefname{codecell}{code}{codes}
\Crefname{codecell}{code}{codes}
% make the text float work with cleverref
\crefname{textcell}{text}{texts}
\Crefname{textcell}{text}{texts}
% make the text float work with cleverref
\crefname{errorcell}{error}{errors}
\Crefname{errorcell}{error}{errors}
""",

    'document_definitions': r"""
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.95}

\lstdefinestyle{mystyle}{
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily,
    breakatwhitespace=false,
    keepspaces=true,
    numbers=left,
    numbersep=10pt,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2,
    breaklines=true,
    literate={\-}{}{0\discretionary{-}{}{-}},
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
}

\lstset{style=mystyle}

\surroundwithmdframed[
  hidealllines=true,
  backgroundcolor=backcolour,
  innerleftmargin=0pt,
  innerrightmargin=0pt,
  innertopmargin=0pt,
  innerbottommargin=0pt]{lstlisting}

""",

    'notebook_input_code': r"""
((( draw_text(cell.metadata,cell.source,"code",
"language=Python,numbers=left,xleftmargin=20pt,xrightmargin=5pt,belowskip=5pt,aboveskip=5pt") )))
""",

    'notebook_output_text': r"""
((( draw_text(cell.metadata,output.data['text/plain'] | strip_ansi,"text",
"language={},postbreak={},numbers=none,xrightmargin=7pt,breakindent=0pt,aboveskip=5pt,belowskip=5pt") )))
""",

    'notebook_output_stream': r"""
((*- if cell.metadata.get("ipub",{}).get("text",{}).use_ansi : -*))
((( draw_text(cell.metadata,output.text | ansi2listings("%") ,"text",
"language={},postbreak={},numbers=none,xrightmargin=7pt,belowskip=5pt,aboveskip=5pt,breakindent=0pt,escapechar=\%") )))
((*- else -*))
((( draw_text(cell.metadata,output.text | strip_ansi ,"text",
"language={},postbreak={},numbers=none,xrightmargin=7pt,belowskip=5pt,aboveskip=5pt,breakindent=0pt") )))
((*- endif *))
""",

    'notebook_output_error': r"""
((( super() )))
""",
    'notebook_output_traceback': """
((( draw_text(cell.metadata,line | indent | strip_ansi,"error",
"language=Python,numbers=none,xrightmargin=5pt,belowskip=2pt,aboveskip=2pt") )))
""",

    'jinja_macros': r"""
((* macro draw_text(meta,source,type,options) -*))

((*- if meta.ipub: -*))

((*- if meta.ipub[type] -*))

((*- if meta.ipub[type].asfloat: -*))
    ((*- if meta.ipub[type].placement: -*))
        ((*- if meta.ipub[type].widefigure: -*))
    \begin{(((type)))cell*}[((meta.ipub[type].placement)))]
        ((*- else -*))
    \begin{(((type)))cell}[(((meta.ipub[type].placement)))]
        ((*- endif *))
    ((*- else -*))
        ((*- if meta.ipub[type].widefigure: -*))
    \begin{(((type)))cell*}
        ((*- else -*))
    \begin{(((type)))cell}
        ((*- endif *))
    ((*- endif *))


    ((* set captionfound = false *))

    ((*- if meta.ipub[type].label: -*))
         ((*- if resources.captions: -*))
             ((*- if resources.captions[meta.ipub[type].label]: -*))
                 \caption{((( resources.captions[meta.ipub[type].label] )))}
                 ((* set captionfound = true *))
             ((*- endif *))
         ((*- endif *))
    ((*- endif *))


    ((*- if captionfound == false -*))
    ((*- if meta.ipub[type].caption: -*))
    \caption{((( meta.ipub[type].caption )))}
    ((*- endif *))
    ((*- endif *))

((*- endif *))

((*- if meta.ipub[type].label: -*))
\label{((( meta.ipub[type].label )))}
((*- endif *))

((*- if meta.ipub[type].format: -*))
\begin{lstlisting}[((( meta.ipub[type].format | dict_to_kwds(options) )))]
((*- else -*))
\begin{lstlisting}[((( options )))]
((*- endif *))
((( source )))
\end{lstlisting}

((*- if meta.ipub[type].asfloat: -*))
\end{(((type)))cell}
((*- endif *))

((*- endif *))

((*- endif *))
((*- endmacro *))
"""

}
