
_This notebook is a chapter of the book ["Generating Software Tests"](https://uds-se.github.io/fuzzingbook/Main.html)._ <br>
<a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Mutation_Fuzzing.ipynb"><img style="float:right" src="https://mybinder.org/badge.svg" alt="Launch Binder (beta)"></a>
[Interactive version (beta)](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Mutation_Fuzzing.ipynb) • 
[Download code](https://uds-se.github.io/fuzzingbook/code/Mutation_Fuzzing.py) • 
[Table of contents](https://uds-se.github.io/fuzzingbook/Main.html) • 
[Change history](https://github.com/uds-se/fuzzingbook/commits/master/notebooks/Mutation_Fuzzing.ipynb) • 
[Issues and comments](https://github.com/uds-se/fuzzingbook/issues) • 
[Main project page](https://github.com/uds-se/fuzzingbook/)
<hr>

# Mutation-Based Fuzzing

Most [randomly generated inputs](Basic_Fuzzing.html) are syntactically _invalid_ and thus are quickly rejected by the processing program.  To exercise functionality beyond input processing, we must increase chances to obtain valid inputs.  One such way is by _mutating_ existing valid inputs - that is, introducing small changes that may still keep the input valid, yet exercise new behavior.

**Prerequisites**

* You should know how basic fuzzing works; for instance, from the ["Fuzzing"](Basic_Fuzzing.html) chapter.

## Fuzzing a URL Parser

Many programs expect their inputs to come in a very specific format before they would actually process them.  As an example, think of a program that accepts a URL (a Web address).  The URL has to be in a valid format (i.e., the URL format) such that the program can deal with it.  When fuzzing with random inputs, what are our chances to actually produce a valid URL?

To get deeper into the problem, let us explore what URLs are made of.  A URL consists of a number of elements:

    scheme://netloc/path?query#fragment
    
where
* `scheme` is the protocol to be used, including `http`, `https`, `ftp`, `file`...
* `netloc` is the name of the host to connect to, such as `www.google.com`
* `path` is the path on that very host, such as `search`
* `query` is a list of key/value pairs, such as `q=fuzzing`
* `fragment` is a marker for a location in the retrieved document, such as `#result`

In Python, we can use the `urlparse()` function to parse and decompose a URL into its parts.


```python
import fuzzingbook_utils
```


```python
try:
    from urlparse import urlparse      # Python 2
except ImportError:
    from urllib.parse import urlparse  # Python 3

urlparse("http://www.google.com/search?q=fuzzing")
```




    ParseResult(scheme='http', netloc='www.google.com', path='/search', params='', query='q=fuzzing', fragment='')



We see how the result encodes the individual parts of the URL in different attributes.

Let us now assume we have a program that takes a URL as input.  To simplify things, we won't let it do very much; we simply have it check the passed URL for validity.  If the URL is valid, it returns True; otherwise, it raises an exception.


```python
def http_program(url):
    supported_schemes = ["http", "https"]
    result = urlparse(url)
    if result.scheme not in supported_schemes:
        raise ValueError("Scheme must be one of " + repr(supported_schemes))
    if result.netloc == '':
        raise ValueError("Host must be non-empty")

    # Do something with the URL
    return True
```

Let us now go and fuzz `http_program()`.  To fuzz, we use the full range of printable ASCII characters, such that `:`, `/`, and lowercase letters are included.


```python
from Basic_Fuzzing import fuzzer
```


```python
fuzzer(char_start=32, char_range=96)
```




    "dyR')'?gtx3m2"



Let's try to fuzz with 1000 random inputs and see whether we have some success.


```python
for i in range(1000):
    try:
        url = fuzzer()
        result = http_program(url)
        print("Success!")
    except ValueError:
        pass
```

What are the chances of actually getting a valid URL?  We need our string to start with `"http://"` or `"https://"`.  Let's take the `"http://"` case first.  That's seven very specific characters we need to start with.  The chances of producing these seven characters randomly (with a character range of 96 different characters) is $1 : 96^7$, or


```python
96 ** 7
```




    75144747810816



The odds of producing a `"https://"` prefix are even worse, at $1 : 96^8$:


```python
96 ** 8
```




    7213895789838336



which gives us a total chance of


```python
likelihood = 1 / (96 ** 7) + 1 / (96 ** 8)
likelihood
```




    1.344627131107667e-14



And this is the number of runs (on average) we'd need to produce a valid URL:


```python
1 / likelihood
```




    74370059689055.02



Let's measure how long one run of `http_program()` takes:


```python
from Timer import Timer
```


```python
trials = 1000
with Timer() as t:
    for i in range(trials):
        try:
            url = fuzzer()
            result = http_program(url)
            print("Success!")
        except ValueError:
            pass

duration_per_run_in_seconds = t.elapsed_time() / trials
duration_per_run_in_seconds
```




    0.00019819698296487333



That's pretty fast, isn't it?  Unfortunately, we have a lot of runs to cover.


```python
seconds_until_success = duration_per_run_in_seconds * (1 / likelihood)
seconds_until_success
```




    14739921453.28825



which translates into


```python
hours_until_success = seconds_until_success / 3600
days_until_success = hours_until_success / 24
years_until_success = days_until_success / 365.25
years_until_success
```




    467.0799253836873



Even if we parallelize things a lot, we're still in for months to years of waiting.  And that's for getting _one_ successful run that will get deeper into `http_program()`.

What basic fuzzing will do well is to test `urlparse()`, and if there is an error in this parsing function, it has good chances of uncovering it.  But as long as we cannot produce a valid input, we are out of luck in reaching any deeper functionality.

## Mutating Inputs

The alternative to generating random strings from scratch is to start with a guiven _valid_ input, and then to subsequently _mutate_ it.  A _mutation_ in this context is a simple string manipulation - say, inserting a (random) character, deleting a character, or flipping a bit in a character representation.  Here are some mutations to get you started:


```python
import random
```


```python
def delete_random_character(s):
    """Returns s with a random character deleted"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    # print("Deleting", repr(s[pos]), "at", pos)
    return s[:pos] + s[pos + 1:]
```


```python
seed_input = "A quick brown fox"
for i in range(10):
    x = delete_random_character(seed_input)
    print(x)
```

    A quik brown fox
    A quick brown fx
    A quick brwn fox
    A quick brown ox
    A quick bown fox
    A quick brown ox
    A quick brownfox
    A quickbrown fox
    Aquick brown fox
    A quick rown fox



```python
def insert_random_character(s):
    """Returns s with a random character inserted"""
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 128))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]
```


```python
for i in range(10):
    print(insert_random_character(seed_input))
```

    A quick brown> fox
    A quick brownU fox
    A quick browHn fox
    A ?quick brown fox
    A (quick brown fox
    A quick bbrown fox
    A quick brown fo}x
    A quick brown fJox
    A quick 2brown fox
    A quick9 brown fox



```python
def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
    return s[:pos] + new_c + s[pos + 1:]

```


```python
for i in range(10):
    print(flip_random_character(seed_input))
```

    A quick brown(fox
    A yuick brown fox
    A yuick brown fox
    A quick brown fOx
    @ quick brown fox
    A quick brown vox
    A quick brown fo|
    A quick brosn fox
    A quick brgwn fox
    A quick brown box


Let us now create a random mutator that randomly chooses which mutation to apply:


```python
mutators = [delete_random_character, insert_random_character, flip_random_character]
```


```python
def mutate(s):
    """Return s with a random mutation applied"""
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(s)
```


```python
for i in range(10):
    print(mutate("A quick brown fox"))
```

    A quick brown fx
    A quick brown Zfox
    A quickw brown fox
    A quick bmrown fox
    A quick /brown fox
    A qqick brown fox
    A quick brownfox
    A quik brown fox
    A quick rown fox
    A quick_ brown fox


The idea is now that _if_ we have some valid input(s) to begin with, we may create more input candidates by applying one of the above mutations.  To see how this works, let's get back to URLs.

## Mutating URLs

Let us now get back to our URL parsing problem.  Let us create a function `is_valid_url()` that checks whether `http_program()` accepts the input.


```python
def is_valid_url(url):
    try:
        result = http_program(url)
        return True
    except ValueError:
        return False
```


```python
assert is_valid_url("http://www.google.com/search?q=fuzzing")
assert not is_valid_url("xyzzy")
```

Let us now apply the `mutate()` function on a given URL and see how many valid inputs we obtain.


```python
seed_input = "http://www.google.com/search?q=fuzzing"
valid_inputs = set()
trials = 20

for i in range(trials):
    inp = mutate(seed_input)
    if is_valid_url(inp):
        valid_inputs.add(inp)
```

We can now observe that by _mutating_ the original input, we get a high proportion of valid inputs:


```python
len(valid_inputs) / trials
```




    0.9



What are the odds of also producing a `https:` prefix by mutating a `http:` sample seed input?  We have to insert ($1 : 3$) the right character `'s'` ($1 : 96$) into the correct position ($1 : l$), where $l$ is the length of our seed input.  This means that on average, we need this many runs:


```python
trials = 3 * 96 * len(seed_input)
trials
```




    10944



We can actually afford this.  Let's try:


```python
from Timer import Timer
```


```python
trials = 0
with Timer() as t:
    while True:
        trials += 1
        inp = mutate(seed_input)
        if inp.startswith("https://"):
            print("Success after", trials, "trials in", t.elapsed_time(), "seconds")
            break
```

    Success after 16905 trials in 0.11996399995405227 seconds


Of course, if we wanted to get, say, an `"ftp://"` prefix, we would need more mutations and more runs – most important, though, we would need to apply _multiple_ mutations.

## Multiple Mutations

So far, we have only applied one single mutation on a sample string.  However, we can also apply _multiple_ mutations, further changing it.  What happens, for instance, if we apply, say, 20 mutations on our sample string?


```python
seed_input = "http://www.google.com/search?q=fuzzing"
mutations = 50
```


```python
inp = seed_input
for i in range(mutations):
    if i % 5 == 0:
        print(i, "mutations:", repr(inp))
    inp = mutate(inp)
```

    0 mutations: 'http://www.google.com/search?q=fuzzing'
    5 mutations: 'http://www.ggle.c/m/cea#rch?q=fuzzing'
    10 mutations: 'htXtp://www.gg,ec-m/cea#rcH?q=fuzzing'
    15 mutations: 'huXtp//www.g,ec-m/cea#rcH?q=fuzzing'
    20 mutations: '3huXtp/ww.g,uc-m/cearcH?q=fuzzing'
    25 mutations: '3huXtp/ww,g,uc-m/cmarc?q?uzzing'
    30 mutations: "3huXtp/ww,g,c-m/cuarc?q?qzzin'"
    35 mutations: "3huXtp/ww=,gc-m/cuarb?qM?qzin'"
    40 mutations: "shXtp/ww=lgsc-m/cuarb?qM?yzin'"
    45 mutations: "shXtp/ww=lgs-m/curb?qM?yzkkn'"


As you see, the original seed input is hardly recognizable anymore.  Mutating the input again and again has the advantage of getting a higher variety in the input, but on the other hand further increases the risk of having an invalid input.  The key to success lies in the idea of _guiding_ these mutations – that is, _keeping those that are especially valuable._

## Guiding by Coverage

To cover as much functionality as possible, one can rely on either _specified_ or _implemented_ functionality, as discussed in the ["Coverage"](Coverage.html) chapter.  For now, we will not assume that there is a specification of program behavior (although it _definitely_ would be good to have one!).  We _will_ assume, though, that the program to be tested exists – and that we can leverage its structure to guide test generation.

Since testing always executes the program at hand, one can always gather information about its execution – the least is the information needed to decide whether a test passes or fails.  Since coverage is frequently measured as well to determine test quality, let us also assume we can retrieve coverage of a test run.  The question is then: _How can we leverage coverage to guide test generation?_

One particularly successful idea is implemented in the popular fuzzer named [_American fuzzy lop_](http://lcamtuf.coredump.cx/afl/), or AFL for short.  Just like our examples above, AFL evolves test cases that have been successful – but for AFL, "success" means _finding a new path through the program execution_.  This way, AFL can keep on mutating inputs that so far have found new paths; and if an input finds another path, it will be retained as well.

We can implement such a strategy by maximizing _diversity in coverage_ in our population.  First, let us create a function `create_candidate()` which randomly picks some input from a given population, and then applies between `min_mutations` and `max_mutations` mutation steps, returning the final result:


```python
def create_candidate(population, min_mutations=2, max_mutations=10):
    candidate = random.choice(population)
    trials = random.randint(min_mutations, max_mutations)
    for i in range(trials):
        candidate = mutate(candidate)
    return candidate
```

Now for the main function.  We maintain a list of inputs (`population`) and a set of coverages already achieved (`coverages_seen`).  The `fuzz()` helper function takes an input and runs the given `function()` on it.  If its coverage is new (i.e. not in `coverages_seen`), the input is added to `population` and the coverage to `coverages_seen`.

The main `coverage_fuzzer()` function first runs `fuzz()` on the provided seed population (adding to the population), and then keeps on creating and testing new candidates coming from `create_candidate()`.


```python
from Coverage import Coverage, population_coverage
```

    importing Jupyter notebook from Coverage.ipynb


    Traceback (most recent call last):
      File "<string>", line 7, in <module>
      File "<string>", line 22, in cgi_decode
    IndexError: string index out of range



```python
def coverage_fuzzer(seed, function, trials=100):
    population = []
    coverages_seen = set()

    def fuzz(inp):
        """Run function(inp) while tracking coverage.  
           If we reach new coverage, 
           add inp to population and its coverage to population_coverage
        """
        nonlocal population  # Access "outer" variables
        nonlocal coverages_seen

        with Coverage() as cov:
            try:
                function(inp)
                valid = True
            except:
                valid = False

        # print(repr(inp))

        new_coverage = frozenset(cov.coverage())
        if valid and new_coverage not in coverages_seen:
            # We have new coverage
            population.append(inp)
            coverages_seen.add(new_coverage)

    for inp in seed:
        fuzz(inp)

    for i in range(trials):
        candidate = create_candidate(population)
        fuzz(candidate)

    return population
```

Let us now put this to use:


```python
seed_input = "http://www.google.com/search?q=fuzzing"
population = coverage_fuzzer(
    seed=[seed_input], function=http_program, trials=1000)
population
```




    ['http://www.google.com/search?q=fuzzing',
     'http://wwwgoogle.co/sarci?q=fu(zzine',
     'http://wwwgoogle.o/sarc,i>q=f(zzLioe',
     'http://wwwgoole.o-src.$q=f(zzLe',
     'http://wwwgoogld.o/sarcU,i,>2q-f(zzLi/oe',
     'http://wwWwgoole.o-src4q=f(zzLe',
     'httP://wwwggogld.o/sarcU,i,>2y-fx(zzLi/oe',
     'http://www.google.cOm.wsearch\x1dfu~zinJg#',
     'httP://wwwggogld&o?sarcUj,i(>2y-f x(zzLi/oe',
     'http://wwwgokogld.Co/sarcU,i,2q-f~zLi/;Roe',
     'httP://wwwggogld&o?sacUj,i(>2y-`x(zzLi/oe',
     'http://wZwnwgoogld.ob/sarcU,i,>2q-f(zzLi;?oe',
     'http://www.goog|e.c\x0fm.wsearch\x1dfu~znJg#',
     'http://wwwgoogld.o/sqrcU,i,>2q-f;(zzLi/oe',
     'httP://wwwggzog#ld.o/sarU,Oi%,>2y-fx(zzLi/oe',
     'http://wwwgoogld$.o/sqrcU,i,2q-f;(zzLi/oe',
     'http://wwwgokogld.Co/sarcU,i,2q-fMzL)/;Ro%',
     'httP://w7Wzwggzog#ld.o/srW,K)%,>2y-fx(zzLi/ou',
     'httP://wwwgaoole.o-rc1.$q@=fzjHe']



Success!  In our population, _each and every input_ now is valid and has a different coverage, coming from various combinations of schemes, paths, queries, and fragments.


```python
cumulative_coverage = population_coverage(population, http_program)

import matplotlib.pyplot as plt
plt.plot(cumulative_coverage)
plt.title('Coverage of urlparse() with random inputs')
plt.xlabel('# of inputs')
plt.ylabel('lines covered');
```

The nice thing about this strategy is that, applied to larger programs, it will happily explore one path after the other – covering functionality after functionality.  All that is needed is a means to capture the coverage.

## Lessons Learned

* Randomly generated inputs are frequently invalid – and thus exercise mostly input processing functionality.
* Mutations from existing valid inputs have much higher chances to be valid, and thus to exercise functionality beyond input processing.


## Next Steps

Our aim is still to sufficiently cover functionality.  From here, we can continue with:

1. Try to cover as much _implemented_ functionality as possible.  To this end, we need to access the program implementation, measure which parts would actually be reached with our inputs, and use this _coverage_ to guide our search.  We will explore this in the next chapter, which discusses [guided mutations](Guided_Mutations.html).

2. Try to cover as much _specified_ functionality as possible.  Here, we would need a _specification of the input format,_ distinguishing between individual input elements such as (in our case) numbers, operators, comments, and strings – and attempting to cover as many of these as possible.  We will explore this as it comes to [grammar-based testing](Grammar_Testing.html), and especially in [grammar-based mutations](Grammar_Mutations.html).

Finally, the concept of a "population" that is systematically "evolved" through "mutations" will be explored in depth when discussing [search-based testing](Search_Based_Testing.html).  Enjoy!


## Exercises


### Exercise 1

Apply the above non-guided mutation-based fuzzing technique on `bc`, using files, as in the chapter ["Introduction to Fuzzing"](Basic_Fuzzing.html).

### Exercise 2

Apply the above guided mutation-based fuzzing technique on `cgi_decode()` from the ["Coverage"](Coverage.html) chapter.  How many trials do you need until you cover all variations of `+`, `%` (valid and invalid), and regular characters?


```python
from Coverage import cgi_decode
```


```python
seed_input = "Hello World"
population = coverage_fuzzer(
    seed=[seed_input], function=cgi_decode, trials=100000)
print(population)
```

    ['Hello World', 'jemQlo+ Wozpl;', 'j%95mwQlow+ WopZd;', 'j%95mwQlow) wopR;']



```python
cumulative_coverage = population_coverage(population, cgi_decode)
```


```python
import matplotlib.pyplot as plt
```


```python
plt.plot(cumulative_coverage)
plt.title('Coverage of cgi_decode() with random inputs')
plt.xlabel('# of inputs')
plt.ylabel('lines covered');
```


![png](Mutation_Fuzzing_files/Mutation_Fuzzing_81_0.png)


### Exercise 3

In this [blog post](https://lcamtuf.blogspot.com/2014/08/binary-fuzzing-strategies-what-works.html), the author of _American Fuzzy Lop_ (AFL), a very popular mutation-based fuzzer discusses the efficiency of various mutation operators.  Implement four of them and evaluate their efficiency as in the examples above.

### Exercise 4

When adding a new element to the list of candidates, AFL does actually not compare the _coverage_, but adds an element if it exercises a new _branch_.  Using branch coverage from the exercises of the ["Coverage"](Coverage.html) chapter, implement this "branch" strategy and compare it against the "coverage" strategy, above.

### Exercise 5

Design and implement a system that will gather a population of URLs from the Web.  Can you achieve a higher coverage with these samples?  What if you use them as intiial population for further mutation?

<hr>

<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">

_This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)._<br>
