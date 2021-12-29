import functools
import time

def timed(f):
    @functools.wraps(f)
    def impl(*args, **kwargs):
        t = time.perf_counter()
        res = f(*args, **kwargs)
        t = time.perf_counter() - t
        print(f'{f.__name__} took {t} seconds')
        return res
    return impl
