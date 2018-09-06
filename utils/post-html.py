#!/usr/bin/env python3
# Expand HEADER and FOOTER elements in generated HTML
# Usage: add-header-and-footer.py CHAPTER_NAME CHAPTER_1 CHAPTER_2 ...

# Note: I suppose this could also be done using Jinja2 templates and ipypublish,
# but this thing here works pretty well.  If you'd like to convert this into some more elegant
# framework, implement it and send me a pull request -- AZ

import argparse
import os.path
import time
import re
import sys

# For icons, see https://fontawesome.com/cheatsheet

menu_start = r"""
<nav>
<div id="cssmenu">
  <ul>
     <li class="has-sub"><a href="https://www.fuzzingbook.org/"><i class="fa fa-fw fa-bars"></i> Generating Software Tests</a>
        <ol>
        <li><a href="https://www.fuzzingbook.org/"><i class="fa fa-fw fa-home"></i> About this book</a>
        <__ALL_CHAPTERS_MENU__>
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
site_footer_template = ""

chapter_header_template = menu_start + r"""
     <li class="has-sub"><a href="https://www.fuzzingbook.org/html/__CHAPTER__.html"><i class="fa fa-fw fa-bars"></i> __CHAPTER_TITLE__</a>
        <ol>
           <__ALL_SECTIONS_MENU__>
        </ol>
     <li><a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/__CHAPTER__.ipynb" target="_blank"><i class="fa fa-fw fa-edit"></i> Open as Notebook</a></li>
     <li><a href="https://www.fuzzingbook.org/code/__CHAPTER__.py"><i class="fa fa-fw fa-download"></i> Code</a></li>
     <li><a href="https://www.fuzzingbook.org/slides/__CHAPTER__.slides.html" target="_blank"><i class="fa fa-fw fa-video-camera"></i> Slides</a></li>
     """ + menu_end

chapter_footer_template = r"""
<p class="imprint">
<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">
This work is licensed under a
<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
&bull;
<a href="https://github.com/uds-se/fuzzingbook/commits/master/notebooks/__CHAPTER__.ipynb")>Last change: __DATE__</a> &bull; 
<a href="https://www.uni-saarland.de/en/footer/dialogue/legal-notice.html">Imprint</a>
</p>
"""

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
parser.add_argument("--site-index", help="omit links to notebook, code, and slides", action='store_true')
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

menu_prefix = args.menu_prefix
if menu_prefix is None:
    menu_prefix = ""

if args.site_index :
    header_template = site_header_template
    footer_template = site_footer_template
else:
    header_template = chapter_header_template
    footer_template = chapter_footer_template

# Construct chapter menu
all_chapters_menu = ""
for menu_ipynb_file in all_chapters:
    basename = os.path.splitext(os.path.basename(menu_ipynb_file))[0]
    title = get_title(menu_ipynb_file)
    menu_html_file = menu_prefix + basename + ".html"
    item = '<li><a href="%s">%s</a></li>\n' % (menu_html_file, title)
    all_chapters_menu += item

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

# sys.exit(0)

# Read it in
print("Reading", chapter_html_file)
chapter_html = open(chapter_html_file, encoding="utf-8").read()

# Replacement orgy
chapter_html = chapter_html \
    .replace(".ipynb", ".html") \
    .replace("\n\n</pre>", "\n</pre>") \
    .replace("<__HEADER__>", header_template) \
    .replace("<__FOOTER__>", footer_template) \
    .replace("__CHAPTER__", chapter) \
    .replace("__CHAPTER_TITLE__", chapter_title) \
    .replace("<__ALL_CHAPTERS_MENU__>", all_chapters_menu) \
    .replace("<__ALL_SECTIONS_MENU__>", all_sections_menu) \
    .replace("__DATE__", time.asctime(time.localtime(notebook_modification_time)))

if args.site_index:
    chapter_html = chapter_html.replace("custom.css", menu_prefix + "/custom.css")

if not args.site_index:
    # The official wauy is set a title in document metadata, 
    # but a) Jupyter Lab can't edit it, and b) the title conflicts with the chapter header
    chapter_html = re.sub(r"<title>.*</title>", "<title>" + chapter_title + "</title>", chapter_html)

# And write it out again
print("Writing", chapter_html_file)
open(chapter_html_file, mode="w", encoding="utf-8").write(chapter_html)
