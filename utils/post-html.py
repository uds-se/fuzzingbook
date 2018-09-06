#!/usr/bin/env python3
# Expand HEADER and FOOTER elements in generated HTML
# Usage: add-header-and-footer.py CHAPTER_NAME CHAPTER_1 CHAPTER_2 ...

import argparse
import os.path
import time

header_template = r"""
<div id="cssmenu">
  <ul>
     <li><a href="http://www.fuzzingbook.org/">Generating Software Tests</a></li>
     <li class="has-sub"><a href="#"><i class="fa fa-fw fa-bars"></i> Chapters</a>
        <ul>
            <!--
           <li class="has-sub"><a href="#">Menu 1</a>
              <ul>
                 <li><a href="#">Menu 1.1</a></li>
                 <li><a href="#">Menu 1.2</a></li>
              </ul>
           </li>
            -->
           <__ALL_CHAPTERS__>
        </ul>
     </li>
     <li><a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/__CHAPTER__.ipynb" target="_blank"><i class="fa fa-fw fa-edit"></i> Open as Notebook</a></li>
     <li><a href="http://www.fuzzingbook.org/code/__CHAPTER__.py"><i class="fa fa-fw fa-download"></i> Code</a></li>
     <li><a href="http://www.fuzzingbook.org/slides/__CHAPTER__.slides.html" target="_blank"><i class="fa fa-fw fa-video-camera"></i> Slides</a></li>
     <li><a href="https://github.com/uds-se/fuzzingbook/" target="_blank"><i class="fa fa-fw fa-git"></i> Project Page</a></li>
  </ul>
</div>
"""

footer_template = r"""
<p class="imprint">
<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">
This work is licensed under a
<a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
&bull;
<a href="https://github.com/uds-se/fuzzingbook/commits/master/notebooks/__CHAPTER__.ipynb")>Last change: __DATE__</a> &bull; 
<a href="https://www.uni-saarland.de/en/footer/dialogue/legal-notice.html">Imprint</a>
</p>
"""

parser = argparse.ArgumentParser()
parser.add_argument("chapter", nargs=1)
parser.add_argument("all_chapters", nargs='*')
args = parser.parse_args()

all_chapters = args.all_chapters
chapter_html_file = args.chapter[0]
chapter = os.path.splitext(os.path.basename(chapter_html_file))[0]
chapter_notebook_file = os.path.join("notebooks", chapter + ".ipynb")
notebook_modification_time = os.path.getmtime(chapter_notebook_file)

print("Reading", chapter_html_file)
chapter_html = open(chapter_html_file, encoding="utf-8").read()

chapter_html = chapter_html \
    .replace(".ipynb", ".html") \
    .replace("<__HEADER__>", header_template) \
    .replace("<__FOOTER__>", footer_template) \
    .replace("\n\n</pre>", "\n</pre>") \
    .replace("__CHAPTER__", chapter) \
    .replace("__DATE__", time.asctime(time.localtime(notebook_modification_time)))

print("Writing", chapter_html_file)
open(chapter_html_file, mode="w", encoding="utf-8").write(chapter_html)
