#!/usr/bin/env python
# -*- coding: utf-8 -*-

tplx_dict = {
    'meta_docstring': 'with the main ipypublish title and contents page setup',

    'document_definitions': """
\\DeclareTranslationFallback{Author}{Author}
\\DeclareTranslation{Portuges}{Author}{Autor}

\\DeclareTranslationFallback{List of Codes}{List of Codes}
\\DeclareTranslation{Catalan}{List of Codes}{Llista de Codis}
\\DeclareTranslation{Danish}{List of Codes}{Liste over Koder}
\\DeclareTranslation{German}{List of Codes}{Liste der Codes}
\\DeclareTranslation{Spanish}{List of Codes}{Lista de C\\'{o}digos}
\\DeclareTranslation{French}{List of Codes}{Liste des Codes}
\\DeclareTranslation{Italian}{List of Codes}{Elenco dei Codici}
\\DeclareTranslation{Dutch}{List of Codes}{Lijst van Codes}
\\DeclareTranslation{Portuges}{List of Codes}{Lista de C\\'{o}digos}

\\DeclareTranslationFallback{Supervisors}{Supervisors}
\\DeclareTranslation{Catalan}{Supervisors}{Supervisors}
\\DeclareTranslation{Danish}{Supervisors}{Vejledere}
\\DeclareTranslation{German}{Supervisors}{Vorgesetzten}
\\DeclareTranslation{Spanish}{Supervisors}{Supervisores}
\\DeclareTranslation{French}{Supervisors}{Superviseurs}
\\DeclareTranslation{Italian}{Supervisors}{Le autorit\\`{a} di vigilanza}
\\DeclareTranslation{Dutch}{Supervisors}{supervisors}
\\DeclareTranslation{Portuguese}{Supervisors}{Supervisores}

""",

    'document_title': r"""

((*- if nb.metadata["ipub"]: -*))

  ((*- if nb.metadata["ipub"]["titlepage"]: -*))

	\begin{titlepage}

	((*- if nb.metadata["ipub"]["titlepage"]["logo"]: -*))
    ((* set filename = nb.metadata.ipub.titlepage.logo | posix_path *))
	\begin{flushright}
		\includegraphics[width=0.7\textwidth]{((( filename )))}
	\end{flushright}
	((*- endif *))

	\begin{center}

	\vspace*{1cm}

	\Huge
	((*- if nb.metadata["ipub"]["titlepage"]["title"]: -*))
	\textbf{((( nb.metadata["ipub"]["titlepage"]["title"] )))}
	((*- else -*))
	\textbf{((( resources.metadata.name | escape_latex )))}
	((*- endif *))

	\vspace{0.5cm}

	((*- if nb.metadata["ipub"]["titlepage"]["subtitle"]: -*))
	\LARGE{((( nb.metadata["ipub"]["titlepage"]["subtitle"] )))}
	((*- endif *))

	\vspace{1.5cm}

	\begin{minipage}{0.8\textwidth}
		\begin{center}
		\begin{minipage}{0.39\textwidth}
		\begin{flushleft} \Large
		\emph{\GetTranslation{Author}:}\\
			((*- if nb.metadata["ipub"]["titlepage"]["author"]: -*))
			((( nb.metadata["ipub"]["titlepage"]["author"] )))\\
			((*- endif *))
			((*- if nb.metadata["ipub"]["titlepage"]["email"]: -*))
			\href{mailto:((( nb.metadata["ipub"]["titlepage"]["email"] )))}{((( nb.metadata["ipub"]["titlepage"]["email"] )))}
			((*- endif *))
		\end{flushleft}
		\end{minipage}
		\hspace{\fill}
		\begin{minipage}{0.39\textwidth}
		\begin{flushright} \Large
			((*- if nb.metadata["ipub"]["titlepage"]["supervisors"]: -*))
			\emph{\GetTranslation{Supervisors}:} \\
			((*- for i in nb.metadata["ipub"]["titlepage"]["supervisors"] *))
			  ((( nb.metadata["ipub"]["titlepage"]["supervisors"][loop.index-1] )))
			((*- endfor *))
			((*- endif *))
		\end{flushright}
		\end{minipage}
		\end{center}
	\end{minipage}

	\vfill

	\begin{minipage}{0.8\textwidth}
	\begin{center}
	((*- if nb.metadata["ipub"]["titlepage"]["tagline"]: -*))
	\LARGE{((( nb.metadata["ipub"]["titlepage"]["tagline"] )))}
	((*- endif *))
	\end{center}
	\end{minipage}

	\vspace{0.8cm}

	((*- if nb.metadata["ipub"]["titlepage"]["institution"]: -*))
		((*- for i in nb.metadata["ipub"]["titlepage"]["institution"] *))
		  \LARGE{((( nb.metadata["ipub"]["titlepage"]["institution"][loop.index-1] )))}\\
		((*- endfor *))
	((*- endif *))

	\vspace{0.4cm}

	\today

	\end{center}
	\end{titlepage}

 ((*- else -*))

	\title{((( resources.metadata.name | escape_latex )))}
	\date{\today}
	\maketitle

 ((*- endif *))

((*- endif *))

""",

    'document_predoc': r"""
((*- if nb.metadata["ipub"]: -*))
    \begingroup
    \let\cleardoublepage\relax
    \let\clearpage\relax
    ((*- if nb.metadata["ipub"]["toc"]: -*))
    \tableofcontents
    ((*- endif *))
    ((*- if nb.metadata["ipub"]["listfigures"]: -*))
    \listoffigures
    ((*- endif *))
    ((*- if nb.metadata["ipub"]["listtables"]: -*))
    \listoftables
    ((*- endif *))
    ((*- if nb.metadata["ipub"]["listcode"]: -*))
    \listof{codecell}{\GetTranslation{List of Codes}}
    ((*- endif *))
    \endgroup
((*- endif *))
"""

}
