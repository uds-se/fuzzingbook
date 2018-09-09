#!/usr/bin/env python3
# Expand HEADER and FOOTER elements in generated HTML
# Usage: add-header-and-footer.py CHAPTER_NAME CHAPTER_1 CHAPTER_2 ...

# Note: I suppose this could also be done using Jinja2 templates and ipypublish,
# but this thing here works pretty well.  If you'd like to convert this into some more elegant
# framework, implement it and send me a pull request -- AZ

import argparse
import os.path
import time
import datetime
import re
import sys
import io
import html

try:
    import nbformat
    have_nbformat = True
except:
    have_nbformat = False
    


# Some fixed strings
booktitle = "Generating Software Tests"
authors = "Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler"
site_html = "https://www.fuzzingbook.org"
github_html = "https://github.com/uds-se/fuzzingbook"
notebook_html = "https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks"

# Book image
bookimage = site_html + "/html/PICS/wordcloud.png"

# Menus
# For icons, see https://fontawesome.com/cheatsheet
menu_start = r"""
<nav>
<div id="cssmenu">
  <ul>
     <li class="has-sub"><a href="__SITE_HTML__/"><i class="fa fa-fw fa-bars"></i> __BOOKTITLE__</a>
        <ol>
           <__ALL_CHAPTERS_MENU__>
        </ol>
     </li>
     <li class="has-sub"><a href="__CHAPTER_HTML__"><i class="fa fa-fw fa-list-ul"></i> __CHAPTER_TITLE__</a>
        <ul>
           <__ALL_SECTIONS_MENU__>
        </ul>
     </li>
     """

menu_end = r"""
     <li class="has-sub"><a href="#"><i class="fa fa-fw fa-comments"></i> Share</a>
        <ul>
            <li><a href="__SHARE_TWITTER__" target=_blank><i class="fa fa-fw fa-twitter"></i> Share on Twitter</a>
            <li><a href="__SHARE_FACEBOOK__" target=_blank><i class="fa fa-fw fa-facebook"></i> Share on Facebook</a>
            <li><a href="__GITHUB_HTML__/issues/" target="_blank"><i class="fa fa-fw fa-commenting"></i> Report an Issue</a></li>
            <li><a href="#citation" id="cite" onclick="revealCitation()"><i class="fa fa-fw fa-mortar-board"></i> Cite</a>
        </ul>
     </li>
  </ul>
</div>
</nav>
"""

site_header_template = menu_start + r"""
     <li class="has-sub"><a href="__CHAPTER_NOTEBOOK_IPYNB__" target="_blank"><i class="fa fa-fw fa-cube"></i> Resources</a>
     <ul>
     <li><a href="__GITHUB_HTML__/" target="_blank"><i class="fa fa-fw fa-github"></i> Project Page</a></li>
     </ul>
     </li>
""" + menu_end

# Chapters
chapter_header_template = menu_start + r"""
     <li class="has-sub"><a href="__CHAPTER_NOTEBOOK_IPYNB__" target="_blank"><i class="fa fa-fw fa-cube"></i> Resources</a>
     <ul>
     <li><a href="__CHAPTER_NOTEBOOK_IPYNB__" target="_blank" class="edit_as_notebook"><i class="fa fa-fw fa-edit"></i> Edit as Notebook</a></li>
     <li><a href="__SITE_HTML__/code/__CHAPTER__.py"><i class="fa fa-fw fa-download"></i> Download Code</a></li>
     <li><a href="__SITE_HTML__/slides/__CHAPTER__.slides.html" target="_blank"><i class="fa fa-fw fa-video-camera"></i> View Slides</a></li>
     <li><a href="__GITHUB_HTML__/" target="_blank"><i class="fa fa-fw fa-github"></i> Project Page</a></li>
     </ul>
     </li>
     """ + menu_end


# Footers
site_citation_template = r"""
<div id="citation" class="citation" style="display: none;">
<a name="citation"></a>
<h2>How to Cite this Work</h2>
<p>
__AUTHORS__: "<a href="__SITE_HTML__">__BOOKTITLE__</a>".  Retrieved __DATE__.
</p>
<pre>
@incollection{fuzzingbook__YEAR__:__CHAPTER__,
    author = {__AUTHORS_BIBTEX__},
    booktitle = {__BOOKTITLE__},
    title = {__BOOKTITLE__},
    year = {__YEAR__},
    publisher = {Saarland University},
    howpublished = {\url{__SITE_HTML__/}},
    note = {Retrieved __DATE__},
    url = {__SITE_HTML__/},
    urldate = {__DATE__}
}
</pre>
</div>
"""

chapter_citation_template = r"""
<div id="citation" class="citation" style="display: none;">
<a name="citation"></a>
<h2>How to Cite this Work</h2>
<p>
__AUTHORS__: "<a href="__CHAPTER_HTML__">__CHAPTER_TITLE__</a>".  In __AUTHORS__ (eds.), "<a href="__SITE_HTML__/">__BOOKTITLE__</a>", <a href="__CHAPTER_HTML__">__CHAPTER_HTML__</a>.  Retrieved __DATE__.
</p>
<pre>
@incollection{fuzzingbook__YEAR__:__CHAPTER__,
    author = {__AUTHORS__},
    booktitle = {__BOOKTITLE__},
    title = {__CHAPTER_TITLE__},
    year = {__YEAR__},
    publisher = {Saarland University},
    howpublished = {\url{__CHAPTER_HTML__}},
    note = {Retrieved __DATE__},
    url = {__CHAPTER_HTML__},
    urldate = {__DATE__}
}
</pre>
</div>
"""

common_footer_template = r"""
<p class="imprint">
<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">
This work is licensed under a
<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target=_blank>Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>
&bull;
<a href="__GITHUB_HTML__/commits/master/notebooks/__CHAPTER__.ipynb" target=_blank)>Last change: __DATE__</a> &bull; 
<a href="#citation" id="cite" onclick="revealCitation()">Cite</a> &bull;
<a href="https://www.uni-saarland.de/en/footer/dialogue/legal-notice.html" target=_blank>Imprint</a>
</p>

<script>
function revealCitation() {
    var c = document.getElementById("citation");
    c.style.display = "block";
}
</script>
"""

chapter_footer_template = common_footer_template + chapter_citation_template
site_footer_template = common_footer_template + site_citation_template


def get_text_contents(notebook):
    if not have_nbformat:
        contents = open(notebook, encoding="utf-8").read()
        contents = re.sub(r'^[^"]*"', "", contents)
        contents = re.sub(r'"^[^"]*$', "", contents)
        return contents

    with io.open(notebook, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    contents = ""
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            contents += "".join(cell.source) + "\n\n"
            
    # print("Contents of", notebook, ": ", repr(contents[:100]))

    return contents
    

def get_title(notebook):
    """Return the title from a notebook file"""
    contents = get_text_contents(notebook)
    match = re.search(r'^# (.*)', contents, re.MULTILINE)
    title = match.group(1).replace(r'\n', '')
    print("Title", title.encode('utf-8'))
    return title

def get_description(notebook):
    """Return the first 2-4 sentences from a notebook file, after the title"""
    contents = get_text_contents(notebook)
    match = re.search(r'^# .*$([^#]*)^#', contents, re.MULTILINE)
    desc = match.group(1).replace(r'\n', '').replace('\n', '')
    desc = re.sub(r"\]\([^)]*\)", "]", desc).replace('[', '').replace(']', '')
    desc = re.sub(r"[_*]", "", desc)
    print("Description", desc.encode('utf-8'))
    return desc

def get_sections(notebook):
    """Return the section titles from a notebook file"""
    contents = get_text_contents(notebook)
    matches = re.findall(r'^# (.*)', contents, re.MULTILINE)
    if len(matches) >= 5:
        # Multiple top sections (book?) - use these
        pass
    else:
        # Use sections instead
        matches = re.findall(r'^## (.*)', contents, re.MULTILINE)
        
    sections = [match.replace(r'\n', '') for match in matches]
    print("Sections", repr(sections).encode('utf-8'))
    return sections
    
    
def anchor(title):
    """Return an anchor '#a-title' for a title 'A title'"""
    return '#' + title.replace(' ', '-')

# Process arguments
parser = argparse.ArgumentParser()
parser.add_argument("--home", help="omit links to notebook, code, and slides", action='store_true')
parser.add_argument("--menu-prefix", help="prefix to html files in menu")
parser.add_argument("chapter", nargs=1)
parser.add_argument("all_chapters", nargs='*')
args = parser.parse_args()

# Get template elements
all_chapters = args.all_chapters
chapter_html_file = args.chapter[0]
chapter = os.path.splitext(os.path.basename(chapter_html_file))[0]
chapter_notebook_file = os.path.join("notebooks", chapter + ".ipynb")
notebook_modification_time = os.path.getmtime(chapter_notebook_file)    
notebook_modification_datetime = datetime.datetime.fromtimestamp(notebook_modification_time) \
    .astimezone().isoformat(sep=' ', timespec='seconds')
notebook_modification_year = repr(datetime.datetime.fromtimestamp(notebook_modification_time).year)

menu_prefix = args.menu_prefix
if menu_prefix is None:
    menu_prefix = ""

if args.home:
    header_template = site_header_template
    footer_template = site_footer_template
else:
    header_template = chapter_header_template
    footer_template = chapter_footer_template

# Construct sections menu
all_sections_menu = ""
basename = os.path.splitext(os.path.basename(chapter_html_file))[0]
chapter_ipynb_file = os.path.join("notebooks", basename + ".ipynb")
chapter_html = site_html + "/html/" + basename + ".html"
chapter_notebook_ipynb = notebook_html + "/" + basename + ".ipynb"

chapter_title = get_title(chapter_ipynb_file)
sections = get_sections(chapter_ipynb_file)
all_sections_menu = ""
for section in sections:
    item = '<li><a href="%s">%s</a></li>\n' % (anchor(section), section)
    all_sections_menu += item


# Construct chapter menu
if args.home:
    link_class = ' class="this_page"'
else:
    link_class = ''
all_chapters_menu = '<li><a href="https://www.fuzzingbook.org/"%s><i class="fa fa-fw fa-home"></i> About this book</a></li>\n' % link_class

for menu_ipynb_file in all_chapters:
    basename = os.path.splitext(os.path.basename(menu_ipynb_file))[0]
    title = get_title(menu_ipynb_file)
    if menu_ipynb_file == chapter_ipynb_file:
        link_class = ' class="this_page"'
    else:
        link_class = ''
    menu_html_file = menu_prefix + basename + ".html"
    item = '<li><a href="%s"%s>%s</a></li>\n' % (menu_html_file, link_class, title)
    all_chapters_menu += item

# Description
description = html.escape(get_description(chapter_ipynb_file))

# Exercises
end_of_exercise = '''
<p><div class="solution_link"><a href="__CHAPTER_NOTEBOOK_IPYNB__#Exercises" target=_blank>Use the notebook</a> to work on the exercises and see solutions.</div></p>
'''

# Sharing
def cgi_escape(text):
    """Produce entities within text."""
    cgi_escape_table = {
        " ": r"%20",
        "&": r"%26",
        '"': r"%22",
        "'": r"%27",
        ">": r"%3e",
        "<": r"%3c",
        ":": r"%3a",
        "/": r"%2f",
        "?": r"%3f",
        "=": r"%3d",
    }
    return "".join(cgi_escape_table.get(c,c) for c in text)

share_twitter = "https://twitter.com/intent/tweet?text=" + \
    cgi_escape(r'I just read "' + chapter_title + '" (part of @FuzzingBook) at ' + chapter_html)
share_facebook = "https://www.facebook.com/sharer/sharer.php?u=" + cgi_escape(chapter_html)


# Authors
def bibtex_escape(authors):
    """Return list of authors in BibTeX-friendly form"""
    tex_escape_table = {
        "ä": r'{\"a}',
        "ö": r'{\"o}',
        "ü": r'{\"u}',
        "Ä": r'{\"A}',
        "Ö": r'{\"O}',
        "Ü": r'{\"U}',
        "ß": r'{\ss}'
    }
    return "".join(tex_escape_table.get(c,c) for c in authors)

authors_bibtex = bibtex_escape(authors).replace(", and ", " and ").replace(", ", " and ")

# sys.exit(0)

# Read it in
print("Reading", chapter_html_file)
chapter_contents = open(chapter_html_file, encoding="utf-8").read()

# Replacement orgy
# 1. Replace all markdown links to .ipynb by .html, such that cross-chapter links work
# 2. Fix extra newlines in cell output produced by ipypublish
# 3. Insert the menus and templates as defined above
chapter_contents = chapter_contents \
    .replace(".ipynb)", ".html)") \
    .replace("\n\n</pre>", "\n</pre>") \
    .replace("<__HEADER__>", header_template) \
    .replace("<__FOOTER__>", footer_template) \
    .replace("<__ALL_CHAPTERS_MENU__>", all_chapters_menu) \
    .replace("<__ALL_SECTIONS_MENU__>", all_sections_menu) \
    .replace("<__END_OF_EXERCISE__>", end_of_exercise) \
    .replace("__BOOKTITLE__", booktitle) \
    .replace("__BOOKIMAGE__", bookimage) \
    .replace("__DESCRIPTION__", description) \
    .replace("__AUTHORS__", authors) \
    .replace("__AUTHORS_BIBTEX__", authors_bibtex) \
    .replace("__CHAPTER__", chapter) \
    .replace("__CHAPTER_TITLE__", chapter_title) \
    .replace("__CHAPTER_HTML__", chapter_html) \
    .replace("__SITE_HTML__", site_html) \
    .replace("__NOTEBOOK_HTML__", notebook_html) \
    .replace("__CHAPTER_NOTEBOOK_IPYNB__", chapter_notebook_ipynb) \
    .replace("__GITHUB_HTML__", github_html) \
    .replace("__SHARE_TWITTER__", share_twitter) \
    .replace("__SHARE_FACEBOOK__", share_facebook) \
    .replace("__DATE__", notebook_modification_datetime) \
    .replace("__YEAR__", notebook_modification_year)

if args.home:
    chapter_contents = chapter_contents.replace("custom.css", menu_prefix + "custom.css")

# Get a title
# The official way is to set a title in document metadata, 
# but a) Jupyter Lab can't edit it, and b) the title conflicts with the chapter header - AZ
chapter_contents = re.sub(r"<title>.*</title>", 
    "<title>" + chapter_title + " - " + booktitle + "</title>", 
    chapter_contents)

# And write it out again
print("Writing", chapter_html_file)
open(chapter_html_file, mode="w", encoding="utf-8").write(chapter_contents)
