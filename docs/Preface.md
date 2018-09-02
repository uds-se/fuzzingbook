
_This notebook is a chapter of the book ["Generating Software Tests"](https://uds-se.github.io/fuzzingbook/Main.html)._ <br>
<a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Preface.ipynb"><img style="float:right" src="https://mybinder.org/badge.svg" alt="Launch Binder (beta)"></a>
[Interactive version (beta)](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Preface.ipynb) • 
[Download code](https://uds-se.github.io/fuzzingbook/code/Preface.py) • 
[Table of contents](https://uds-se.github.io/fuzzingbook/Main.html) • 
[Change history](https://github.com/uds-se/fuzzingbook/commits/master/notebooks/Preface.ipynb) • 
[Issues and comments](https://github.com/uds-se/fuzzingbook/issues) • 
[Main project page](https://github.com/uds-se/fuzzingbook/)
<hr>

# Preface

Software has bugs.  This book addresses this problem by automated software testing, specifically by showing how to _generate tests automatically_.  Such generated tests can be extended into ordinary tests, by adding code that checks for correct behavior; or be used for "fuzzing", that is, finding inputs that cause a program to crash, hang, or otherwise malfunction.  The aim is to exercise a maximum of functionality with a minimum of effort.

The book is designed as a textbook for a course in software testing; or as supplementary material in a software testing or software engineering course; and as a resource for software developers.

The main characteristics of this book are:

* It assumes that the reader's goal is to achieve a maximum of software reliability with a minimum of cost, automating test generation and execution as much as possible;

* It presents a set of practical techniques that can be immediately put to use on a large variety of software, presenting and discussing executable source code for all techniques;

* It places software test generation techniques in a coherent framework, allowing the techniques to dovetail and integrate with each other.

## Why this book?

Software test generation brings software quality to a new level.  Not only are we talking about automatically _executing_ software tests (as with unit testing), but actually _producing_ software tests automatically.  In contrast to the simple generation of random inputs (or "fuzzing"), we discuss test generation techniques that adhere to the input language, that systematically cover code structure, and that even are able to automatically learn the input language of the program under test.  These novel techniques lead to dramatic improvements in test generation and software testing, and they now are mature enough to be assembled in a book - even with executable code.

## Who is this book for?

* _Students_ who read this book will gain a deep understanding of common practices in software test generation, and may use these techniques to extend and adapt them as part of their research.
* _Developers_ who read this book will not only gain the same understanding, but will also be able to use the techniques for their own projects, adapting and extending the code samples provided.
* _Technical managers_ will get insights into the capabilities (and limitations) of software test and test generation, and may want to integrate test generation into their own testing workflows.

## Book formats

This book comes in four formats:

1. As a set of _HTML pages_ to view in your browser (free)
2. As a set of _Python modules_ to try out examples yourself (free)
3. As a set of _Jupyter notebooks_, which you can edit, interact with, and derive the above formats from, as well as others such as slides or Word files (free).
4. As a _printed book or PDF_ (available for purchase)

For self-teaching, the HTML pages may be fine; for offline reading, we'd rather recommend the printed book or PDF.  For teaching, we recommend the Notebook format, as you can easily interact with them, and extend the material for your own purposes.

## How to read this book

This book allows for selective reading.  There are a few units in the beginning that define central concepts (and code modules) for others; but after that, units are set to be as independent as possible from each other.

\todo{Add possible paths thorugh the book once all chapters are there.}

<hr>

<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">

_This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)._<br>
