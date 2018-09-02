
_This notebook is a chapter of the book ["Generating Software Tests"](https://uds-se.github.io/fuzzingbook/Main.html)._ <br>
<a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Guide_for_Authors.ipynb"><img style="float:right" src="https://mybinder.org/badge.svg" alt="Launch Binder (beta)"></a>
[Interactive version (beta)](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Guide_for_Authors.ipynb) • 
[Download code](https://uds-se.github.io/fuzzingbook/code/Guide_for_Authors.py) • 
[Table of contents](https://uds-se.github.io/fuzzingbook/Main.html) • 
[Change history](https://github.com/uds-se/fuzzingbook/commits/master/notebooks/Guide_for_Authors.ipynb) • 
[Issues and comments](https://github.com/uds-se/fuzzingbook/issues) • 
[Main project page](https://github.com/uds-se/fuzzingbook/)
<hr>

# Guide for Authors

This workbook compiles the most important conventions for all book chapters.


## Organization of this Book

### Chapters  as Notebooks

Each chapter comes in its own _Jupyter notebook_.  A single notebook (= a chapter) should cover the material (text and code, possibly slides) for a 90-minute lecture.

A chapter notebook should be named `Topic.ipynb`, where `Topic` is the topic.  `Topic` must be usable as a Python module, so `Topic` should:

* start with an upercase letter
* consist of letters and underscores (`_`) only
* should use underscores (`_`) to separate words.

All non-notebook files and folders come with lowercase letters; this may make it easier to differentiate them.

Notebooks are stored in the `notebooks` folder.

### Output Formats

The notebooks by themselves can be used by instructors and students to toy around with.  They can edit code (and text) as they like and even run them as a slide show.

The notebook can be _exported_ to multiple (non-interactive) formats:

* HTML – for placing this material online.
* PDF – for printing (and selling :-)
* Python – for coding
* Slides – for presenting

The default export options already do a good job in producing these formats; however, there also is a Makefile that generates all of these automatically.

### The Book

The book is compiled automatically from the individual notebooks.  Each notebook becomes a chapter; references are compiled in the final chapter.

## Creating and Building

### Tools you will need

To work on the notebook files, you need the following:

1. Jupyter notebook.  The easiest way to install this is via the [Anaconda distribution](https://www.anaconda.com/download/).

2. Once you have the Jupyter notebook installed, you can start editing and coding right away by starting `jupyter notebook` in the topmost folder.

3. If (like me) you don't like the Jupyter Notebook interface, there's two alternatives I can recommend:
    * [Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/) is the designated successor to Jupyter Notebook.  Invoke it as `jupyter lab`.  It comes with a much more modern interface, but misses autocompletion and a couple of extensions.  I am running it [as a Desktop application](http://christopherroach.com/articles/jupyterlab-desktop-app/) which gets rid of all the browser toolbars.
    * On the Mac, the [Pineapple app](https://nwhitehead.github.io/pineapple/) integrates a nice editor with a local server.  This is easy to use, but misses a few features; also, it hasn't seen updates since 2015.

4. To create the entire book (with citations, references, and all), you also need the [ipybublish](https://github.com/chrisjsewell/ipypublish) package.  This allows you to merge multiple chapters into a single PDF or HTML file, create slides, and more.  A Makefile provides the essential tools for creation.


### Version Control

We use git in a single strand of revisions.  Do not branch, do not merge. Sync early; sync often.  Only push if everything ("make all") builds and passes.


The [nbdime](https://github.com/jupyter/nbdime) package gives you tools such as `nbdiff` (and even better, `nbdiff-web`) to compare notebooks against each other; this ensures that cell _contents_ are compared rather than the binary format.


`nbdime config-git --enable` integrates nbdime with git such that `git diff` runs the above tools; merging should also be notebook-specific.

### Creating Derived Formats (HTML, PDF, code, ...)

The [Makefile](../Makefile) provides rules for all targets.  Type `make help` for instructions.

The Makefile should work with GNU make and a standard Jupyter Notebook installation.  To create the multi-chapter book and BibTeX citation support, you need to install the  [iPyPublish](https://github.com/chrisjsewell/ipypublish) package (which includes the `nbpublish` command).

### Creating a New Chapter

To create a new chapter for the book,

1. Set up a new `.ipynb` notebook file as copy of [Template.ipynb](Template.html).

2. Include it in the `CHAPTERS` list in the `Makefile`

3. Add it to the git repository.

## Coding

### Set up

The first code block in each notebook should be


```python
import fuzzingbook_utils
```

This sets up stuff such that notebooks can import each other's code (see below). This import statement is removed in the exported Python code, as the .py files would import each other directly.

### Coding Style and Consistency

We use Python 3 (specifically, Python 3.5) for all code.  If you can, try to write code that can be easily backported to Python 2.

We use standard Python coding conventions according to [PEP 8](https://www.python.org/dev/peps/pep-0008/).

Use one cell for each definition or example.  During importing, this makes it easier to decide which cells to import (see below).

Your code must pass the `pycodestyle` style checks which you get by invoking `make style`.  The `code prettify` notebook extension allows you to automatically make your code adhere to PEP 8.

In the book, this is how we denote `variables`, `functions()`, `Classes`, `Notebooks`, `variables_and_constants`, `EXPORTED_CONSTANTS`, `'characters'`, `"strings"`, and `<grammar-elements>`.

Beyond simple syntactical things, here's a [very nice guide](https://docs.python-guide.org/writing/style/) to get you started writing "pythonic" code.


### Design and Architecture

Stick to simple functions and data types.  We want our readers to focus on functionality, not Python.  You are encouraged to write in a "pythonic" style, making use of elegant Python features such as list comprehensions, sets, and more; however, if you do so, be sure to explain the code such that readers familiar with, say, C or Java can still understand things.

Avoid object orientation – in notebooks, you can only define classes as a whole, which clashes with the notebook style of incrementally developing a program.

### Importing Code from Notebooks

To import the code of individual notebooks, you can import directly from .ipynb notebook files.


```python
from Basic_Fuzzing import fuzzer
```


```python
fuzzer(100, ord('0'), 10)
```




    '570584828819316243132848597283919858758117492298765524367745690463660251326732298'



**Important**: When importing a notebook, the module loader will **only** load cells that start with

* a function definition (`def`)
* a class definition (`class`)
* a variable definition if all uppercase (`ABC = 123`)
* `import` and `from` statements

All other cells are _ignored_ to avoid recomputation of notebooks and clutter of `print()` output.

The exported Python code will import from the respective .py file instead.  (There's no filtering here as with notebooks, so you'll see plenty of output when importing.)

Import modules only as you need them, such that you can motivate them well in the text.

## Helpers

There's a couple of notebooks with helpful functions, including [Timer](Timer.html), [ExpectError and ExpectTimeout](ExpectError.html).  Also check out the [Coverage](Coverage.html) class.

### Quality Assurance

In your code, make use of plenty of assertions that allow to catch errors quickly.

### Issue Tracker

The GitLab project page allows to enter and track issues.

## Writing Text

Text blocks use Markdown syntax.  [Here is a handy guide](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).


### Sections

Any chapter notebook must begin with `# TITLE`, and sections and subsections should then follow by `## SECTION` and `### SUBSECTION`.

Sections should start with their own block, to facilitate cross-referencing.


### Highlighting

Use

* _emphasis_ for highlighting,
* `backticks` for code and other verbatim elements.


### Hyphens and Dashes

Use – for em-dashes, - for hyphens, and $-$ for minus.

### Lists and Enumerations

You can use bulleted lists:

* Item A
* Item B

and enumerations:

1. item 1
1. item 2

For description lists, use a combination of bulleted lists and highlights:

* **PDF** is great for reading offline
* **HTML** is great for reading online



### Math

LaTeX math formatting works, too.

`$x = \sum_{n = 1}^{\infty}\frac{1}{n}$` gets you
$x = \sum_{n = 1}^{\infty}\frac{1}{n}$.


### Inline Code

Python code normally goes into its own cells, but you can also have it in the text:

```python
s = "Python syntax highlighting"
print s
```

## Images

To insert images, use Markdown syntax `![Andreas Zeller](PICS/Zeller.jpg){width=100%}` inserts a picture from the `PICS` folder.

![Andreas Zeller](PICS/Zeller.jpg){width=100%}

All pictures go to `PICS/`, both in source as well as derived formats; both are stored in git, too.  (Not all of us have all tools to recreate diagrams, etc.)

## Floating Elements and References

\todo[inline]{I haven't gotten this to work yet -- AZ}

To produce floating elements in LaTeX and PDF, edit the metadata of the cell which contains it. (In the Jupyter Notebook Toolbar go to View -> Cell Toolbar -> Edit Metadata and a button will appear above each cell.) This allows you to control placement and create labels.

### Floating Figures

Edit metadata as follows:

```json
{
"ipub": {
  "figure": {
    "caption": "Figure caption.",
    "label": "fig:flabel",
    "placement": "H",
	"height":0.4,
    "widefigure": false,
    }
  }
}
```

- all tags are optional
- height/width correspond to the fraction of the page height/width, only one should be used (aspect ratio will be maintained automatically)
- `placement` is optional and constitutes using a placement arguments for the figure (e.g. \begin{figure}[H]). See [Positioning_images_and_tables](https://www.sharelatex.com/learn/Positioning_images_and_tables).
- `widefigure` is optional and constitutes expanding the figure to the page width (i.e. \begin{figure*}) (placement arguments will then be ignored)


### Floating Tables

For  **tables** (e.g. those output by `pandas`), enter in cell metadata:

```json
{
"ipub": {
     "table": {
	    "caption": "Table caption.",
	    "label": "tbl:tlabel",
	    "placement": "H",
            "alternate": "gray!20"
	  }
   }
}
```

- `caption` and `label` are optional
- `placement` is optional and constitutes using a placement arguments for the table (e.g. \begin{table}[H]). See [Positioning_images_and_tables](https://www.sharelatex.com/learn/Positioning_images_and_tables).
- `alternate` is optional and constitutes using alternating colors for the table rows (e.g. \rowcolors{2}{gray!25}{white}). See (https://tex.stackexchange.com/a/5365/107738)[https://tex.stackexchange.com/a/5365/107738].
- if tables exceed the text width, in latex, they will be shrunk to fit 


### Floating Equations

For  **equations** (e.g. those output by `sympy`), enter in cell metadata:

```json
{
  "ipub": {
	  "equation": {
        "environment": "equation",
	    "label": "eqn:elabel"
	  }
  }
}
```

- environment is optional and can be 'none' or any of those available in [amsmath](https://www.sharelatex.com/learn/Aligning_equations_with_amsmath); 'equation', 'align','multline','gather', or their \* variants. Additionaly, 'breqn' or 'breqn\*' will select the experimental [breqn](https://ctan.org/pkg/breqn) environment to *smart* wrap long equations. 
- label is optional and will only be used if the equation is in an environment


### References

To reference to a floating object, use `\cref`, e.g. \cref{eq:texdemo}



## Cross-Referencing

###  Section References

* To refer to sections in the same notebook, use the header name as anchor, e.g. 
`[Code](#Code)` gives you [Code](#Code).  For multi-word titles, replace spaces by hyphens (`-`), as in [Using Notebooks as Modules](#Using-Notebooks-as-Modules).

* To refer to cells (e.g. equations or figures), you can define a label as cell metadata.  See [Floating Elements and References](#Floating-Elements-and-References) for details.

* To refer to other notebooks, use a Markdown cross-reference to the notebook file, e.g. [the "Fuzzing" chapter](Basic_Fuzzing.html).  A special script will be run to take care of these links.  Reference chapters by name, not by number.

### Citations

To cite papers, cite in LaTeX style: `\cite{purdom1972}`, which gets you \cite{purdom1972}.  The keys refer to BibTeX entries in [fuzzingbook.bib](fuzzingbook.bib).  

* LaTeX/PDF output will have a "References" section appended.
* HTML output will link to the URL field from the BibTeX entry. Be sure it points to the DOI.

## Todo's

* To mark todo's, use `\todo{Thing to be done}.`  \todo{Expand this}

## Tables

Tables with fixed contents can be produced using Markdown syntax:

| Tables | Are | Cool |
| ------ | ---:| ----:|
| Zebra  | 2   |   30 |
| Gnu    | 20  |  400 |


If you want to produce tables from Python data, the `PrettyTable` package (included in the book) allows to [produce tables with LaTeX-style formatting.](http://blog.juliusschulz.de/blog/ultimate-ipython-notebook)


```python
import numpy as np
import fuzzingbook_utils.PrettyTable as pt

data = np.array([[1, 2, 30], [2, 3, 400]])
pt.PrettyTable(data, [r"$\frac{a}{b}$", r"$b$", r"$c$"], print_latex_longtable=False)
```




<table><tr><td>$\frac{a}{b}$</td><td>$b$</td><td>$c$</td></tr><tr><td>1</td><td>2</td><td>30</td></tr><tr><td>2</td><td>3</td><td>400</td></tr></table>



## Plots and Data

It is possible to include plots in notebooks.  Here is an example of plotting a function:


```python
%matplotlib inline

import matplotlib.pyplot as plt

x = np.linspace(0, 3 * np.pi, 500)
plt.plot(x, np.sin(x ** 2))
plt.title('A simple chirp');
```


![png](Guide_for_Authors_files/Guide_for_Authors_45_0.png)


And here's an example of plotting data:


```python
%matplotlib inline

import matplotlib.pyplot as plt
data = [25, 36, 57]
plt.plot(data)
plt.title('Increase in data');
```


![png](Guide_for_Authors_files/Guide_for_Authors_47_0.png)


Plots are available in all derived versions (HTML, PDF, etc.)

## Slides

You can set up the notebooks such that they also can be presented as slides.  In the browser, select View -> Cell Toolbar -> Slideshow.  You can then select a slide type for each cell:

* `New slide` starts a new slide with the cell
* `Sub-slide` starts a new slide (which you navigate "down" to)
* `Fragment` is a cell that gets revealed after a click
* `Skip` is skipped during the slide show
* `Notes` goes into presenter notes

To create slides, do `make slides`; to view them, change into the `slides/` folder and open the created HTML files.  (The `reveal.js` package has to be in the same folder as the slide to be presented.)

I am not sure how many people will use the notebooks as slide shows, but it comes as a nice extra.



(Hint: In a slide presentation, type `s` to see presenter notes.)

## Writing Tools

When you're editing in the browser, you may find these extensions helpful:  [Jupyter Notebook Extensions](https://github.com/ipython-contrib/jupyter_contrib_nbextensions) is a collection of productivity-enhancing tools (including spellcheckers).

I found these extensions to be particularly useful:

  * Code prettify (to produce "nice" syntax)
  
  * Codefolding
  
  * Live Markdown Preview (while you're editing)
  
  * Spell Checker (while you're editing)
  
  * Table of contents (for quick navigation)

## Interaction

It is possible to include interactive elements in a notebook, as in the following example:

```python
try:
    from ipywidgets import interact, interactive, fixed, interact_manual

    x = interact(fuzzer, char_start=(32, 128), char_range=(0, 96))
except ImportError:
    pass
```

Note that such elements will be present in the notebook versions only, but not in the HTML and PDF versions, so use them sparingly (if at all).  To avoid errors during production of derived files, protect against `ImportError` exceptions as in the above example.

## Read More

Here is some documentation on the tools we use:

1. [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) - general introduction to Markdown

1. [iPyPublish](https://github.com/chrisjsewell/ipypublish) - rich set of tools to create documents with citations and references




## Alternative Tool Sets

We don't currently use these, but they are worth learning:

1. [Making Publication-Ready Python Notebooks](http://blog.juliusschulz.de/blog/ultimate-ipython-notebook) - Another tool set on how to produce book chapters from notebooks

1. [Writing academic papers in plain text with Markdown and Jupyter notebook](https://sylvaindeville.net/2015/07/17/writing-academic-papers-in-plain-text-with-markdown-and-jupyter-notebook/) - Alternate ways on how to generate citations

1. [A Jupyter LaTeX template](https://gist.github.com/goerz/d5019bedacf5956bcf03ca8683dc5217#file-revtex-tplx) - How to define a LaTeX template

1. [Boost Your Jupyter Notebook Productivity](https://towardsdatascience.com/jupyter-notebook-hints-1f26b08429ad) - a collection of hints for debugging and profiling Jupyter notebooks



<hr>

<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">

_This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)._<br>
