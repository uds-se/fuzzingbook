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

# For icons, see https://fontawesome.com/cheatsheet

menu_start = r"""
<nav>
<div id="cssmenu">
  <ul>
     <li class="has-sub"><a href="https://www.fuzzingbook.org/"><i class="fa fa-fw fa-bars"></i> Generating Software Tests</a>
        <ol>
           <__ALL_CHAPTERS_MENU__>
        </ol>
     </li>
     <li class="has-sub"><a href="https://www.fuzzingbook.org/html/__CHAPTER__.html"><i class="fa fa-fw fa-bars"></i> __CHAPTER_TITLE__</a>
        <ol>
           <__ALL_SECTIONS_MENU__>
        </ol>
     </li>
     """

menu_end = r"""
     <li><a href="https://github.com/uds-se/fuzzingbook/" target="_blank"><i class="fa fa-fw fa-git"></i> Project Page</a></li>
  </ul>
</div>
</nav>
"""

site_header_template = menu_start + menu_end
site_footer_template = r"""
<p class="imprint">
<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">
This work is licensed under a
<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target=_blank>Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>
&bull;
<a href="https://github.com/uds-se/fuzzingbook/commits/master/notebooks/__CHAPTER__.ipynb" target=_blank)>Last change: __DATE__</a> &bull; 
<a href="#citation" id="cite" onclick="toggleCitation()">Cite</a> &bull;
<a href="https://www.uni-saarland.de/en/footer/dialogue/legal-notice.html" target=_blank>Imprint</a>
</p>

<script>
function toggleCitation() {
    var c = document.getElementById("citation");
    if (c.style.display === "none") {
        c.style.display = "block";
    } else {
        c.style.display = "none";
    }
}
</script>

<div id="citation" class="citation" style="display: none;">
<a name="citation"></a>
<h2>How to Cite this Work</h2>
<p>
Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler: "<a href="https://www.fuzzingbook.org/slides/__CHAPTER__.html">__CHAPTER_TITLE__</a>".  In Zeller, Gopinath, Böhme, Fraser, and Holler (eds.), "<a href="https://www.fuzzingbook.org/">Generating Software Tests</a>", <a href="https://www.fuzzingbook.org/slides/__CHAPTER__.html">https://www.fuzzingbook.org/slides/__CHAPTER__.html</a>.  Retrieved __DATE__.
</p>
<pre>
@incollection{fuzzingbook__YEAR__:__CHAPTER__,
    author = {Andreas Zeller and Rahul Gopinath and Marcel B{\"o}hme and Gordon Fraser and Christian Holler},
    booktitle = {Generating Software Tests},
    title = {__CHAPTER_TITLE__},
    year = {__YEAR__},
    publisher = {Saarland University},
    howpublished = {\url{https://www.fuzzingbook.org/html/__CHAPTER__.html}},
    note = {Retrieved __DATE__},
    url = {https://www.fuzzingbook.org/html/__CHAPTER__.html},
    urldate = {__DATE__}
}
</pre>
</div>
"""

chapter_header_template = menu_start + r"""
     <li><a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/__CHAPTER__.ipynb" target="_blank"><i class="fa fa-fw fa-edit"></i> Open as Notebook</a></li>
     <li><a href="https://www.fuzzingbook.org/code/__CHAPTER__.py"><i class="fa fa-fw fa-download"></i> Code</a></li>
     <li><a href="https://www.fuzzingbook.org/slides/__CHAPTER__.slides.html" target="_blank"><i class="fa fa-fw fa-video-camera"></i> Slides</a></li>
     """ + menu_end

chapter_footer_template = site_footer_template

def get_title(notebook):
    """Return the title from a notebook file"""
    contents = open(notebook, encoding="utf-8").read()
    match = re.search(r'"# (.*)"', contents)
    return match.group(1).replace(r'\n', '')

def get_sections(notebook):
    """Return the section titles from a notebook file"""
    contents = open(notebook, encoding="utf-8").read()
    matches = re.findall(r'"## (.*)"', contents)
    return [match.replace(r'\n', '') for match in matches]
    
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


# sys.exit(0)

# Read it in
print("Reading", chapter_html_file)
chapter_html = open(chapter_html_file, encoding="utf-8").read()

# Replacement orgy
# 1. Replace all markdown links to .ipynb by .html, such that cross-chapter links work
# 2. Fix extra newlines in cell output produced by ipypublish
# 3. Insert the menus and templates as defined above
chapter_html = chapter_html \
    .replace(".ipynb)", ".html)") \
    .replace("\n\n</pre>", "\n</pre>") \
    .replace("<__HEADER__>", header_template) \
    .replace("<__FOOTER__>", footer_template) \
    .replace("__CHAPTER__", chapter) \
    .replace("__CHAPTER_TITLE__", chapter_title) \
    .replace("<__ALL_CHAPTERS_MENU__>", all_chapters_menu) \
    .replace("<__ALL_SECTIONS_MENU__>", all_sections_menu) \
    .replace("__DATE__", notebook_modification_datetime) \
    .replace("__YEAR__", notebook_modification_year)

if args.home:
    chapter_html = chapter_html.replace("custom.css", menu_prefix + "custom.css")

# Get a title
# The official way is to set a title in document metadata, 
# but a) Jupyter Lab can't edit it, and b) the title conflicts with the chapter header - AZ
chapter_html = re.sub(r"<title>.*</title>", "<title>" + chapter_title + " - Generating Software Tests</title>", chapter_html)

# And write it out again
print("Writing", chapter_html_file)
open(chapter_html_file, mode="w", encoding="utf-8").write(chapter_html)
