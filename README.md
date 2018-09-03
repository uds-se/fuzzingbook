# Generating Software Tests

__Welcome to "[Generating Software Tests](http://www.fuzzingbook.org/html/Main.html)"!__  This book teaches how to automate _software testing_, specifically by showing how to _generate tests automatically_.  Such generated tests can be extended into ordinary tests, by adding code that checks for correct behavior; or be used for "fuzzing", that is, finding inputs that cause a program to crash, hang, or otherwise malfunction.


## Breaking Software for Fun and Profit

This work is designed as a _textbook_ for a course in software testing; as _supplementary material_ in a software testing or software engineering course; and as a _resource for software developers_. We cover random fuzzing, mutation-based fuzzing, grammar-based test generation, symbolic testing, and much more, illustrating all techniques with code examples that you can try out yourself.


## A Textbook for Paper, Screen, and Keyboard

You can use this book in three ways:

* You can __[read chapters in your browser](http://www.fuzzingbook.org/html/Main.html)__.  Go to the [table of contents](http://www.fuzzingbook.org/html/Main.html), or start right away with the [preface](http://www.fuzzingbook.org/html/Preface.html) or [introduction to fuzzing](http://www.fuzzingbook.org/html/Basic_Fuzzing.html).  All code is available for download.

* You can __interact with chapters as Jupyter Notebooks__ (beta).  This allows you change and extend with the code, experimenting _live in your browser._  Just click on "Open as interactive notebook" at the top of each chapter.  [Try interacting with the introduction to fuzzing.](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepathnnotebooks/Basic_Fuzzing.ipynb)

* You can __present chapters as slides__ (beta).  This allows for presenting the material in lectures.  Just click on "View slides" at the top of each chapter. [Try viewing slides on the introduction to fuzzing.](http://www.fuzzingbook.org/slides/Basic_Fuzzing.slides.html)

This book is _work in progress,_ with new chapters coming out every week.  To get notified when a new chapter comes out, <a href="https://twitter.com/FuzzingBook?ref_src=twsrc%5Etfw" data-show-count="false">follow us on Twitter</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>. 
<a href="https://twitter.com/FuzzingBook?ref_src=twsrc%5Etfw" class="twitter-follow-button" data-show-count="false">Follow @FuzzingBook on Twitter</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>




## News

<a class="twitter-timeline" href="https://twitter.com/FuzzingBook?ref_src=twsrc%5Etfw">FuzzingBook news</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>



## About the Authors

This book is written by _Andreas Zeller, Rahul Gopinath, Marcel Böhme, Gordon Fraser, and Christian Holler_.  All of us are long-standing experts in software testing and test generation; and we have written or contributed to some of the most important test generators and fuzzers on the planet.  As an example, if you are reading this in a Firefox, Chrome, or Edge Web browser, you can do so safely partly because of us, as _the very techniques listed in this book have found more than 2,600 bugs in their JavaScript interpreters so far._  We are happy to share our expertise and making it accessible to the public.


## Frequently Asked Questions

### Which content will be coming up?

The contents of this book will include topics such as:

1. Introduction to Testing
2. Basic Fuzzing
3. Coverage
4. Mutation-Based Fuzzing
5. Grammar-Based Fuzzing
6. Fuzzing Function Calls
7. Fuzzing User Interfaces
8. Parsing and Mutating Inputs
9. Search-Based Testing
10. Symbolic Testing
11. Mining Grammars
12. Probabilistic Testing
13. Carving Unit Tests
14. Fuzzing and Invariants
15. Protection and Repair

See the [table of contents](http://www.fuzzingbook.org/html/Main.html) for those chapters that are already done.


### Why does it take so long to start an interactive notebook?

We use the [binder](https://mybinder.org) service, which runs notebooks on their own servers.  Starting Jupyter through binder normally takes about 30 seconds. If, however, you are the first to invoke binder after a book update, binder recreates its environment, which can take a few minutes.  Note, though, that binder is officially in beta and we do not have control over binder.


### I have a comment or a suggestion.  What do I do?

Report an issue on the [development page](https://github.com/uds-se/fuzzingbook/issues).


### I have reported an issue two weeks ago.  When will it be addressed?

We prioritize issues as follows:

1. Bugs in code published on fuzzingbook.org
2. Bugs in text published on fuzzingbook.org
3. Writing missing chapters
4. Issues in yet unpublished code or text
5. Issues related to development or construction
6. Things marked as "beta"
7. Everything else


### How can I solve problems myself?

We're glad you ask that.  The [development page](https://github.com/uds-se/fuzzingbook/) has all sources and some supplementary material.  Pull requests that fix issues are very welcome.


### How can I contribute?

Again, we're glad you're here!  See our [Guide for Authors](http://www.fuzzingbook.org/html/Guide_for_Authors.html) for instructions on coding and writing.


### Do you provide PDFs of your material?

At this point, we do not provide support for PDF versions.  We are working on producing PDF and paper versions once the book is complete.


<hr>

<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">

All work on this site is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
