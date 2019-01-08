import time

"""
Function used to track time that functions take to finish.
Function timing is used as annotation, example

@timing
def test_fun:
    pass
    
"""


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap
