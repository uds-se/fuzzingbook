<!-- Fuzzingbook README -->

<!-- Badges to be shown on project page -->

[![Python Tests](https://github.com/uds-se/fuzzingbook/actions/workflows/check-code.yml/badge.svg)](https://github.com/uds-se/fuzzingbook/actions/workflows/check-code.yml)
&nbsp;
[![Notebook Tests](https://github.com/uds-se/fuzzingbook/actions/workflows/check-notebooks.yml/badge.svg)](https://github.com/uds-se/fuzzingbook/actions/workflows/check-notebooks.yml)
&nbsp;
[![Static Type Checking](https://github.com/uds-se/fuzzingbook/actions/workflows/check-types.yml/badge.svg)](https://github.com/uds-se/fuzzingbook/actions/workflows/check-types.yml)
&nbsp;
[![Imports](https://github.com/uds-se/fuzzingbook/actions/workflows/check-imports.yml/badge.svg)](https://github.com/uds-se/fuzzingbook/actions/workflows/check-imports.yml)
&nbsp;
[![Website www.fuzzingbook.org](https://img.shields.io/website-up-down-green-red/https/www.fuzzingbook.org.svg)](https://www.fuzzingbook.org/)

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=docs/notebooks/00_Table_of_Contents.ipynb)
&nbsp;
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://www.python.org/)
&nbsp;
[![Made with Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange.svg)](https://www.jupyter.org/)
&nbsp;
[![License: MIT (Code), CC BY-NC-SA (Book)](https://img.shields.io/badge/License-MIT_(Code),_CC_BY--NC--SA_4.0_(Book)-blue.svg)](https://github.com/uds-se/fuzzingbook/blob/master/LICENSE.md)

# About this Book

__Welcome to "The Fuzzing Book"!__ 
Software has bugs, and catching bugs can involve lots of effort.  This book addresses this problem by _automating_ software testing, specifically by _generating tests automatically_.  Recent years have seen the development of novel techniques that lead to dramatic improvements in test generation and software testing.  They now are mature enough to be assembled in a book – even with executable code. 


```python
from bookutils import YouTubeVideo
YouTubeVideo("w4u5gCgPlmg")
```





<a href="https://www.youtube-nocookie.com/embed/w4u5gCgPlmg" target="_blank">
<img src="https://www.fuzzingbook.org/html/PICS/youtube.png" width=640>
</a>
        



## A Textbook for Paper, Screen, and Keyboard

You can use this book in four ways:

* You can __read chapters in your browser__.  Check out the list of chapters in the menu above, or start right away with the [introduction to testing](https://www.fuzzingbook.org/html/Intro_Testing.html) or the [introduction to fuzzing](https://www.fuzzingbook.org/html/Fuzzer.html).  All code is available for download.

* You can __interact with chapters as Jupyter Notebooks__ (beta).  This allows you to edit and extend the code, experimenting _live in your browser._  Simply select "Resources → Edit as Notebook" at the top of each chapter. <a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/HEAD?labpath=docs/notebooks/Fuzzer.ipynb" target=_blank>Try interacting with the introduction to fuzzing.</a>

* You can __use the code in your own projects__.  You can download the code as Python programs; simply select "Resources → Download Code" for one chapter or "Resources → All Code" for all chapters.  These code files can be executed, yielding (hopefully) the same results as the notebooks.  Even easier: [Install the fuzzingbook Python package](https://www.fuzzingbook.org/html/Importing.html).

* You can __present chapters as slides__.  This allows for presenting the material in lectures.  Just select "Resources → View slides" at the top of each chapter. <a href="https://www.fuzzingbook.org/slides/Fuzzer.slides.html" target=_blank>Try viewing the slides for the introduction to fuzzing.</a>

## Who this Book is for

This work is designed as a _textbook_ for a course in software testing or security testing; as _supplementary material_ in a software testing, security testing, or software engineering course; and as a _resource for software developers_. We cover random fuzzing, mutation-based fuzzing, grammar-based test generation, symbolic testing, and much more, illustrating all techniques with code examples that you can try out yourself.

## News

This book is _work in progress._  All chapters planned are out now, but we keep on refining text and code with [minor and major releases.](https://www.fuzzingbook.org/html/ReleaseNotes.html)  To get notified on updates, <a href="https://mastodon.social/@TheFuzzingBook">follow us on Mastodon</a>.

<!--
