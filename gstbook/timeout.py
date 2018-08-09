#!/usr/bin/env python
# Portable timeout decorator
# Not very efficient, but should work on all platforms

__all__ = [ "timeout", "Timeout" ]

import sys
import time

try:
    # Should be defined in Python 3
    x = TimeoutError
except:
    # For Python 2
    class TimeoutError(Exception):
        def __init__(self, value = "Timeout"):
            self.value = value
        def __str__(self):
            return repr(self.value)

end_time = 0

def check_time(frame, event, arg):
    global end_time
    
    current_time = time.time()
    # print(end_time - current_time, "seconds left")
    if current_time >= end_time:
        raise TimeoutError
        
    return check_time

# Decorator
def timeout(seconds_before_timeout):
    def decorate(f):

        def new_f(*args, **kwargs):
            global end_time
            
            start_time = time.time()
            end_time   = start_time + seconds_before_timeout
            
            old_trace = sys.gettrace()
            try:
                sys.settrace(check_time)
                result = f(*args, **kwargs)
            finally:
                sys.settrace(old_trace)
            return result
        return new_f

    return decorate

# Class
class Timeout(object):
    def __init__(self, seconds):
        self.seconds_before_timeout = seconds
        pass
        
    def __enter__(self):
        # print("Enter")
        global end_time

        start_time = time.time()
        end_time   = start_time + self.seconds_before_timeout
        # print("End time:", end_time)

        self.old_trace = sys.gettrace()
        sys.settrace(check_time)
        
    def __exit__(self, exc_type, exc_value, traceback):
        # print("Exit")
        self.cancel()

    def cancel(self):
        sys.settrace(self.old_trace)



if __name__ == "__main__":
    
    import traceback
    
    def test():
        print("Start")
        for i in range(10):
            time.sleep(1)
            print(i, "seconds have passed")
    

    # Variant 1: With decorators
    @timeout(5)
    def decorator_test():
        test()

    # Variant 2: With object
    def object_test():
        with Timeout(5):
            test()
            
    for f in [decorator_test, object_test]:
        print(repr(f))
        try:
            f()
        except:
            traceback.print_exc()
