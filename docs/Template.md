
_This notebook is a chapter of the book ["Generating Software Tests"](https://uds-se.github.io/fuzzingbook/Main.html)._ <br>
<a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Template.ipynb"><img style="float:right" src="https://mybinder.org/badge.svg" alt="Launch Binder (beta)"></a>
[Interactive version (beta)](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Template.ipynb) • 
[Download code](https://uds-se.github.io/fuzzingbook/code/Template.py) • 
[Table of contents](https://uds-se.github.io/fuzzingbook/Main.html) • 
[Change history](https://github.com/uds-se/fuzzingbook/commits/master/notebooks/Template.ipynb) • 
[Issues and comments](https://github.com/uds-se/fuzzingbook/issues) • 
[Main project page](https://github.com/uds-se/fuzzingbook/)
<hr>

# _Title_

_Brief abstract/introduction/motivation.  State what the chapter is about in 1-2 paragraphs._

_If you set a title here, also set it up in the notebook metadata, such that it also appears in the PDF cover._

**Prerequisites**

* _Refer to earlier chapters as notebooks here, as here:_ [Earlier Chapter](Basic_Fuzzing.html).

## _Section 1_

\todo{Add}

## _Section 2_

\todo{Add}

## _Section 3_

\todo{Add}

_If you want to introduce code, it is helpful to state the most important functions, as in:_

* `random.randrange(start, end)` - return a random number [`start`, `end`]
* `range(start, end)` - create a list with integers from `start` to `end`.  Typically used in iterations.
* `for elem in list: body` executes `body` in a loop with `elem` taking each value from `list`.
* `for i in range(start, end): body` executes `body` in a loop with `i` from `start` to `end` - 1.
* `chr(n)` - return a character with ASCII code `n`


```python
import fuzzingbook_utils
```


```python
# More code
```


```python
# Even more code
```

## _Section 4_

\todo{Add}

## Lessons Learned

* _Lesson one_
* _Lesson two_
* _Lesson three_

## Next Steps

_Link to subsequent chapters (notebooks) here, as in:_

* [use _mutations_ on existing inputs to get more valid inputs](Mutation_Fuzzing.html)
* [use _grammars_ (i.e., a specification of the input format) to get even more valid inputs](Grammars.html)
* [reduce _failing inputs_ for efficient debugging](Reducing.html)


## Exercises

_Close the chapter with a few exercises such that people have things to do.  Use the Jupyter `Exercise2` nbextension to add solutions that can be interactively viewed or hidden.  (Alternatively, just copy the exercise and solution cells below with their metadata.)  We will set up things such that solutions do not appear in the PDF and HTML formats._

### Exercise 1

_Text of the exercise_

_Solution for the exercise_

<hr>

<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">

_This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)._<br>
