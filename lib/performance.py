import functools
import time

def _pretty_duration(t):
    if t < 100:
        return f'{t} seconds'

    parts = []
    minutes, seconds = divmod(t, 60)
    hours, minutes = divmod(int(minutes), 60)
    if hours > 0:
        parts.append('1 hour' if hours == 1 else f'{hours} hours')
    if minutes > 0:
        parts.append('1 minute' if minutes == 1 else f'{minutes} minutes')
    if seconds > 0:
        parts.append('1 second' if seconds == 1 else f'{seconds} seconds')
    return ', '.join(parts)

def timed(f):
    @functools.wraps(f)
    def impl(*args, **kwargs):
        t = time.perf_counter()
        res = f(*args, **kwargs)
        t = time.perf_counter() - t
        
        print(f'{f.__name__} took {_pretty_duration(t)}')
        return res
    return impl
