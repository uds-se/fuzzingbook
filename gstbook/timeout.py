#!/usr/bin/env python
# Portable timeout decorator
# Not very efficient, but should work on all platforms

__all__ = [ "timeout" ]

import sys
import time

# class TimeoutError(Exception):
#     def __init__(self, value = "Timeout"):
#         self.value = value
#     def __str__(self):
#         return repr(self.value)

end_time = 0

def timeout(seconds_before_timeout):
    def decorate(f):
        def check_time(frame, event, arg):
            global end_time
            
            current_time = time.time()
            if current_time >= end_time:
                raise TimeoutError
            return check_time

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


if __name__ == "__main__":
    @timeout(5)
    def mytest():
        print("Start")
        for i in range(10):
            time.sleep(1)
            print(i, "seconds have passed")

    mytest()
