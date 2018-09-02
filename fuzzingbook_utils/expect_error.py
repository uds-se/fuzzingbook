#!/usr/bin/env python
# Decorator that checks and reports errors, while continuing execution.
# Useful to demonstrate (expected) errors in notebooks.

__all__ = [ "expect_error", "ExpectError" ]

import traceback

# Decorator
def expect_error(f):
    def new_f(*args, **kwargs):
        result = None
        try:
            result = f(*args, **kwargs)
        except:
            traceback.print_exc()
        return result
    return new_f

# Class
class ExpectError(object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        # End of `with` clause
        if exc_type is None:
            # No exception
            return
            
        # An exception occurred - print it
        traceback.print_exception(exc_type, exc_value, tb)
        return True # Ignore it

if __name__ == "__main__":
    
    def test():
        # Trigger an exception
        x = 1 / 0

    # Variant 1: With decorators
    @expect_error
    def decorator_test():
        test()

    # Variant 2: With object
    def object_test():
        with ExpectError():
            test()

    print("Start")
    
    for f in [decorator_test, object_test]:
        print(repr(f))
        f()
        
    print("End")
