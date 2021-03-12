tplx_dict = {
    'meta_docstring': 'with the main ipypublish article setup',

    'document_docclass': r"""
	\documentclass[10pt,parskip=half,
	toc=sectionentrywithdots,
	bibliography=totocnumbered,
	captions=tableheading,numbers=noendperiod]{scrartcl}

((*- if nb.metadata.ipub: *))
((*- if nb.metadata.ipub.language: *))
%\usepackage{polyglossia}
%\setmainlanguage{((( nb.metadata.ipub.language )))}
%\DeclareTextCommandDefault{\nobreakspace}{\leavevmode\nobreak\ }
\usepackage[((( nb.metadata.ipub.language )))]{babel}
((*- endif *))
((*- endif *))

""",

    'document_margins': r"""
 % Used to adjust the document margins
\usepackage{geometry}
\geometry{tmargin=1in,bmargin=1in,lmargin=1in,rmargin=1in,
nohead,includefoot,footskip=25pt}
% you can use showframe option to check the margins visually
""",

    'document_packages': r"""
    \usepackage{translations}
	\usepackage{microtype} % improves the spacing between words and letters
	\usepackage{placeins} % placement of figures
    % could use \usepackage[section]{placeins} but placing in subsection in command section
	% Places the float at precisely the location in the LaTeX code (with H)
	\usepackage{float}
	\usepackage[colorinlistoftodos,obeyFinal,textwidth=.8in]{todonotes} % to mark to-dos
	% number figures, tables and equations by section
	\usepackage{chngcntr}
	% header/footer
	\usepackage[footsepline=0.25pt]{scrlayer-scrpage}
""",

    'document_definitions': r"""
    \setcounter{secnumdepth}{5}

    % Colors for the hyperref package
    \definecolor{urlcolor}{rgb}{0,.145,.698}
    \definecolor{linkcolor}{rgb}{.71,0.21,0.01}
    \definecolor{citecolor}{rgb}{.12,.54,.11}

""",

    'document_commands': r"""
	% ensure new section starts on new page
	\addtokomafont{section}{\clearpage}

    % Prevent overflowing lines due to hard-to-break entities
    \sloppy

    % Setup hyperref package
    \hypersetup{
      breaklinks=true,  % so long urls are correctly broken across lines
      colorlinks=true,
      urlcolor=urlcolor,
      linkcolor=linkcolor,
      citecolor=citecolor,
      }

    % ensure figures are placed within subsections
    \makeatletter
    \AtBeginDocument{%
      \expandafter\renewcommand\expandafter\subsection\expandafter
        {\expandafter\@fb@secFB\subsection}%
      \newcommand\@fb@secFB{\FloatBarrier
        \gdef\@fb@afterHHook{\@fb@topbarrier \gdef\@fb@afterHHook{}}}%
      \g@addto@macro\@afterheading{\@fb@afterHHook}%
      \gdef\@fb@afterHHook{}%
    }
    \makeatother

	% number figures, tables and equations by section
	\usepackage{chngcntr}
	\counterwithout{figure}{section}
	\counterwithout{table}{section}
	\counterwithout{equation}{section}
	\makeatletter
	\@addtoreset{table}{section}
	\@addtoreset{figure}{section}
	\@addtoreset{equation}{section}
	\makeatother
	\renewcommand\thetable{\thesection.\arabic{table}}
	\renewcommand\thefigure{\thesection.\arabic{figure}}
	\renewcommand\theequation{\thesection.\arabic{equation}}

    ((*- if nb.metadata.ipub: *))

        % set global options for float placement
        \makeatletter
          \providecommand*\setfloatlocations[2]{\@namedef{fps@#1}{#2}}
        \makeatother

        ((*- if nb.metadata.ipub.table: -*))
        ((*- if nb.metadata.ipub.table.placement: *))

        \setfloatlocations{table}{((( nb.metadata.ipub.table.placement )))}

        ((*- endif *))
        ((*- endif *))
        ((*- if nb.metadata.ipub.figure: -*))
        ((*- if nb.metadata.ipub.figure.placement: *))

        \setfloatlocations{figure}{((( nb.metadata.ipub.figure.placement )))}

        ((*- endif *))
        ((*- endif *))

    ((*- endif *))

    % align captions to left (indented)
	\captionsetup{justification=raggedright,
	singlelinecheck=false,format=hang,labelfont={it,bf}}

	% shift footer down so space between separation line
	\ModifyLayer[addvoffset=.6ex]{scrheadings.foot.odd}
	\ModifyLayer[addvoffset=.6ex]{scrheadings.foot.even}
	\ModifyLayer[addvoffset=.6ex]{scrheadings.foot.oneside}
	\ModifyLayer[addvoffset=.6ex]{plain.scrheadings.foot.odd}
	\ModifyLayer[addvoffset=.6ex]{plain.scrheadings.foot.even}
	\ModifyLayer[addvoffset=.6ex]{plain.scrheadings.foot.oneside}
	\pagestyle{scrheadings}
	\clearscrheadfoot{}
	\ifoot{\leftmark}
	\renewcommand{\sectionmark}[1]{\markleft{\thesection\ #1}}
	\ofoot{\pagemark}
	\cfoot{}

""",

    'document_header_end': r"""
% clereref must be loaded after anything that changes the referencing system
\usepackage{cleveref}
\creflabelformat{equation}{#2#1#3}
"""

}
