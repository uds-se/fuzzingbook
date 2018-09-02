

def extend_class(cls):
    """
    Given class cls, apply decorator @extend_class to function f so
    that f becomes a regular method of cls:

    >>> class cls: pass

    >>> @extend_class(cls)
    ... def f(self):
    ...   pass

    Extending class has several usages:

    1 There are classes A, B, ... Z, all defining methods foo and bar.
      Though the usual approach is to group the code around class
      definitions in files A.py, B.py, ..., Z.py, it is sometimes more
      convenient to group all definitions of A.foo(), B.foo(), ... up
      to Z.foo(), in one file "foo.py", and all definitions of bar in
      file "bar.py".

    2 Another usage of @extend_class is building a class step-by-step
      --- first creating an empty class, and later populating it with
      methods.

    3 Finally, it is possible to @extend several classes
      simultaneously with the same method, as in the example below,
      where classes A and B share method foo.

    >>> class A: pass  # empty class
    ...
    >>> class B: pass  # empty class
    ...
    >>> @extend_class(A)
    ... @extend_class(B)
    ... def foo(self,s):
    ...     print s
    ...
    >>> a = A()
    >>> a.foo('hello')
    hello
    >>> b = B()
    >>> b.foo('world')
    world

    LIMITATIONS

    1. @extend_class won't work on builtin classes, such as int.
    2. Not tested on python 3.

    AUTHOR

    victorlei@gmail.com
    """
    return lambda f: (setattr(cls,f.__name__,f) or f)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
