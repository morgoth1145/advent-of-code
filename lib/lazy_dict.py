import collections

class _LazyDict(collections.defaultdict):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def __missing__(self, key):
        val = self.fn(key)
        self[key] = val
        return val

def make_lazy_dict(fn):
    return _LazyDict(fn)
