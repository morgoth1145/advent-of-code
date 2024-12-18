def bisect(low, high, predicate):
    '''Finds the first index in the range [low, high) where the predicate
    is satisfied. Returns -1 if it is never satisifed.'''
    if low+1 >= high:
        return -1
    if not predicate(high-1):
        return -1
    if predicate(low):
        return low

    bad = low
    good = high-1

    while bad+1 < good:
        mid = (bad + good) // 2
        if predicate(mid):
            good = mid
        else:
            bad = mid

    return good
