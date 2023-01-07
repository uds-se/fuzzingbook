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

* You can __interact with chapters as Jupyter Notebooks__ (beta).  This allows you to edit and extend the code, experimenting _live in your browser._  Simply select "Resources → Edit as Notebook" at the top of each chapter. <a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=docs/notebooks/Fuzzer.ipynb" target=_blank>Try interacting with the introduction to fuzzing.</a>

* You can __use the code in your own projects__.  You can download the code as Python programs; simply select "Resources → Download Code" for one chapter or "Resources → All Code" for all chapters.  These code files can be executed, yielding (hopefully) the same results as the notebooks.  Even easier: [Install the fuzzingbook Python package](https://www.fuzzingbook.org/html/Importing.html).

* You can __present chapters as slides__.  This allows for presenting the material in lectures.  Just select "Resources → View slides" at the top of each chapter. <a href="https://www.fuzzingbook.org/slides/Fuzzer.slides.html" target=_blank>Try viewing the slides for the introduction to fuzzing.</a>

## Who this Book is for

This work is designed as a _textbook_ for a course in software testing; as _supplementary material_ in a software testing or software engineering course; and as a _resource for software developers_. We cover random fuzzing, mutation-based fuzzing, grammar-based test generation, symbolic testing, and much more, illustrating all techniques with code examples that you can try out yourself.

## News

This book is _work in progress._  All chapters planned are out now, but we keep on refining the material with [minor and major releases.](https://www.fuzzingbook.org/html/ReleaseNotes.html)  To get notified on updates, <a href="https://twitter.com/FuzzingBook?ref_src=twsrc%5Etfw" data-show-count="false">follow us on Twitter</a>.

<a class="twitter-timeline" data-width="500" data-chrome="noheader nofooter noborders transparent" data-link-color="#A93226" data-align="center" href="https://twitter.com/FuzzingBook?ref_src=twsrc%5Etfw" data-dnt="true">News from @FuzzingBook</a> 


## About the Authors

This book is written by _Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler_.  All of us are long-standing experts in software testing and test generation; and we have written or contributed to some of the most important test generators and fuzzers on the planet.  As an example, if you are reading this in a Firefox, Chrome, or Edge Web browser, you can do so safely partly because of us, as _the very techniques listed in this book have found more than 2,600 bugs in their JavaScript interpreters so far._  We are happy to share our expertise and making it accessible to the public.

## Frequently Asked Questions

### Troubleshooting

#### Why does it take so long to start an interactive notebook?

The interactive notebook uses the [mybinder.org](https://mybinder.org) service, which runs notebooks on their own servers.  Starting Jupyter through mybinder.org normally takes about 30 seconds, depending on your Internet connection. If, however, you are the first to invoke binder after a book update, binder recreates its environment, which will take a few minutes.  Reload the page occasionally.

#### The interactive notebook does not work!

mybinder.org imposes a [limit of 100 concurrent users for a repository](https://mybinder.readthedocs.io/en/latest/user-guidelines.html).  Also, as listed on the [mybinder.org status and reliability page](https://mybinder.readthedocs.io/en/latest/reliability.html),

> As mybinder.org is a research pilot project, the main goal for the project is to understand usage patterns and workloads for future project evolution. While we strive for site reliability and availability, we want our users to understand the intent of this service is research and we offer no guarantees of its performance in mission critical uses.

There are alternatives to mybinder.org; see below.

#### Do I have alternatives to the interactive notebook?

If mybinder.org does not work or match your needs, you have a number of alternatives:

1. **Download the Python code** (using the menu at the top) and edit and run it in your favorite environment.  This is easy to do and does not require lots of resources.

2. **Download the Jupyter Notebooks** (using the menu at the top) and open them in Jupyter.  Here's [how to install jupyter notebook on your machine](https://www.dataquest.io/blog/jupyter-notebook-tutorial/).

3. **Run the notebook locally** in a Docker container. For more information, see [How to use the book with Docker](https://github.com/uds-se/fuzzingbook/blob/master/deploy/README.md).  

4. If you want to use the book in a classroom, and depend on your users having access to the interactive notebooks, consider using or deploying a [JupyterHub](http://jupyter.org/hub) or [BinderHub](https://github.com/jupyterhub/binderhub) instance.

#### Can I run the code on my Windows machine?

We try to keep the code as general as possible, but occasionally, when we interact with the operating system, we assume a Unix-like environment (because that is what Binder provides).  To run these examples on your own Windows machine, you can install a Linux VM or a [Docker environment](https://github.com/uds-se/fuzzingbook/blob/master/deploy/README.md).

#### Can't you run your own dedicated cloud service?

Technically, yes; but this would cost money and effort, which we'd rather spend on the book at this point.  If you'd like to host a [JupyterHub](http://jupyter.org/hub) or [BinderHub](https://github.com/jupyterhub/binderhub) instance for the public, please _do so_ and let us know.

### Content

#### Can I use your code in my own programs?

Yes!  See the [installation instructions](https://www.fuzzingbook.org/html/Importing.html) for details.

#### Which content has come up?

See the [release notes](https://www.fuzzingbook.org/html/ReleaseNotes.html) for details.

#### How do I cite your work?

Thanks for referring to our work!  Once the book is complete, you will be able to cite it in the traditional way.  In the meantime, just click on the "cite" button at the bottom of the Web page for each chapter to get a citation entry.

#### Can you cite my paper?  And possibly write a chapter about it?

We're always happy to get suggestions!  If we missed an important reference, we will of course add it.  If you'd like specific material to be covered, the best way is to _write a notebook_ yourself; see our [Guide for Authors](https://www.fuzzingbook.org/html/Guide_for_Authors.html) for instructions on coding and writing.  We can then refer to it or even host it.

### Teaching and Coursework

#### Can I use your material in my course?

Of course!  Just respect the [license](https://github.com/uds-se/fuzzingbook/blob/master/LICENSE.md) (including attribution and share alike).  If you want to use the material for commercial purposes, contact us.

#### Can I extend or adapt your material?

Yes!  Again, please see the [license](https://github.com/uds-se/fuzzingbook/blob/master/LICENSE.md) for details.

#### How can I run a course based on the book?

We have successfully used the material in various courses.  

* Initially, we used the slides and code and did _live coding_ in lectures to illustrate how a technique works. 

* Now, the goal of the book is to be completely self-contained; that is, it should work without additional support.  Hence, we now give out completed chapters to students in a _flipped classroom_ setting, with the students working on the notebooks at their leisure.  We would meet in the classroom to discuss experiences with past notebooks and discuss future notebooks.

* We have the students work on exercises from the book or work on larger (fuzzing) projects.  We also have students who use the book as a base for their research; indeed, it is very easy to prototype in Python for Python.

When running a course, [do not rely on mybinder.org](#Troubleshooting) – it will not provide sufficient resources for a larger group of students.  Instead, [install and run your own hub.](#Do-I-have-alternatives-to-the-interactive-notebook?)

#### Are there specific subsets I can focus on?

We have compiled a number of [tours through the book](https://www.fuzzingbook.org/html/Tours.html) for various audiences.  Our [Sitemap](https://www.fuzzingbook.org/html/00_Table_of_Contents.html) lists the dependencies between the individual chapters.

#### How can I extend or adapt your slides?

Download the Jupyter Notebooks (using the menu at the top) and adapt the notebooks at your leisure (see above), including "Slide Type" settings.  Then,

1. Download slides from Jupyter Notebook; or
2. Use the RISE extension ([instructions](http://www.blog.pythonlibrary.org/2018/09/25/creating-presentations-with-jupyter-notebook/)) to present your slides right out of Jupyter notebook.

#### Do you provide PDFs of your material?

At this point, we do not provide support for PDF versions.  We will be producing PDF and print versions after the book is complete.

### Other Issues

#### I have a question, comment, or a suggestion.  What do I do?

You can [tweet to @fuzzingbook on Twitter](https://twitter.com/fuzzingbook), allowing the community of readers to chime in.  For bugs that you'd like to get fixed, report an issue on the [development page](https://github.com/uds-se/fuzzingbook/issues).

#### I have reported an issue two weeks ago.  When will it be addressed?

We prioritize issues as follows:

1. Bugs in code published on fuzzingbook.org
2. Bugs in text published on fuzzingbook.org
3. Writing missing chapters
4. Issues in yet unpublished code or text
5. Issues related to development or construction
6. Things marked as "beta"
7. Everything else

#### How can I solve problems myself?

We're glad you ask that.  The [development page](https://github.com/uds-se/fuzzingbook/) has all sources and some supplementary material.  Pull requests that fix issues are very welcome.

#### How can I contribute?

Again, we're glad you're here!  We are happy to accept 

* **Code fixes and improvements.**  Please place any code under the MIT license such that we can easily include it.
* **Additional text, chapters, and notebooks** on specialized topics.  We plan to set up a special folder for third-party contributions.

See our [Guide for Authors](https://www.fuzzingbook.org/html/Guide_for_Authors.html) for instructions on coding and writing.
