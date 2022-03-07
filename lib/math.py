import collections
import functools
import math

def mod_mult_inv(n, mod):
    '''Calculates and returns the modular multiplicative inverse of n % mod
    such that (n * n_inv) % mod == 1
    '''
    return pow(n, -1, mod)

def minimum_divisors_to_make_coprime(a, b):
    '''Calculates the divisors of a and b such that gcd(a // a_div, b // b_div)
    is 1 and a_div * b_div == gcd(a, b).
    '''
    if b < a:
        # Prefer a being the smaller value. It can make the iteration faster.
        b_div, a_div = minimum_divisors_to_make_coprime(b, a)
        return a_div, b_div

    a_div = math.gcd(a, b)
    b_div = 1
    # a // a_div may still share divisors with b. Find them and shift them to
    # b_div. This may take multiple iterations for some cases (such as
    # a = 27 and b = 9 where the minimum divisors are a_div = 1 and b_div = 9)
    # since gcd(a // a_div, a_div) may not detect the full extent of the
    # conflict. (For a = 27 and b = 9, a_div starts at 9 so gcd(a // a_div, a_div)
    # is only 3, not 9!)
    while True:
        still_present = math.gcd(a // a_div, a_div)
        if still_present == 1:
            return a_div, b_div
        a_div //= still_present
        b_div *= still_present

def chinese_remainder(congruencies):
    '''Efficiently calculates and returns the smallest number which works for
    all given congruences. For example, given the following:
    x % 5 == 2
    x % 7 == 3
    x % 11 == 8
    The smallest x which satisfies all three is 52.
    If no solution exists, returns None.

    Arguments:
    congruencies -- The list of congruencies to use. Expected to be a list of
    (mod, remainder) tuples.
    '''
    n = 1
    rem = 0
    for mod, r in congruencies:
        n_div, mod_div = minimum_divisors_to_make_coprime(n, mod)
        common_denom = n_div * mod_div
        if common_denom > 1:
            # n and mod are not coprime, check for conflicts
            if rem % common_denom != r % common_denom:
                # There are no solutions as the congruences conflict
                # That is, the first congruence (sol % n == rem) and the
                # second congruence (sol % mod == r) imply *different* answers
                # mod common_denom!
                return None

            # These congruencies can be reduced to be coprime using the divisors
            # computed above
            if n_div != 1:
                n //= n_div
                rem %= n
            if mod_div != 1:
                mod //= mod_div
                r %= mod

        next_n = n*mod
        mod_inv = mod_mult_inv(mod, n)
        n_inv = mod_mult_inv(n, mod)
        # Given two congruences: (x % mod == a) and (x % q == b)
        # If mod and q are coprime then multiplicative inverses exist such that
        # mod*mod_inv % q == 1 and q*q_inv % mod == 1
        # We can construct the following
        # y = (a*q*q_inv + b*mod*mod_inv) % (mod*q)
        # Then y % mod == a and y % q == b. Thus y is a solution
        # We can then merge these into a "super congruence" and merge in the next one!
        next_rem = (rem*mod*mod_inv + r*n*n_inv) % next_n
        n = next_n
        rem = next_rem
    # The final remainder is the smallest number which works for all congruencies!
    return rem

def offset_chinese_remainder(congruencies):
    '''Efficiently calculates and returns the smallest number which works for
    all given *offset* congruences. For example, given the following:
    (x + 2) % 5 == 0
    (x + 3) % 7 == 0
    (x + 8) % 11 == 0
    The smallest x which satisfies all three is 52.
    If no solution exists, returns None.

    Arguments:
    congruencies -- The list of congruencies to use. Expected to be a list of
    (mod, offset) tuples.
    '''
    # Convert congruencies to chinese remainder form
    congruencies = [(mod, (mod - (offset % mod)) % mod)
                    for mod, offset
                    in congruencies]
    return chinese_remainder(congruencies)

def chinese_remainder_incongruence(incongruencies):
    '''Efficiently calculates and returns the smallest number which works for
    all given incongruences. For example, given the following:
    x % 4 != 0
    x % 2 != 1
    x % 6 != 2
    x % 6 != 0
    The smallest x which satisfies all three is 10.
    If no solution exists, returns None.

    Arguments:
    incongruencies -- The list of incongruencies to use. Expected to be a list
    of (mod, remainder) tuples.
    '''
    mod_to_bad_remainders = collections.defaultdict(set)

    for mod, remainder in incongruencies:
        mod_to_bad_remainders[mod].add(remainder % mod)

    valid_congruency_options = [
        (mod, set(range(mod)) - bad_remainders)
        for mod, bad_remainders
        in mod_to_bad_remainders.items()
    ]

    # Process valid congruency options from the fewest to greatest
    # number of options to minimize exponential blow-up during processing
    valid_congruency_options.sort(key=lambda pair: (len(pair[1]), pair[0]))

    # Follow the same overall algorithm as chinese_remainder, but keep track
    # of sets of options instead of one answer.
    n = 1
    rem_options = {0}

    for mod, r_options in valid_congruency_options:
        new_options = set()

        n_div, mod_div = minimum_divisors_to_make_coprime(n, mod)
        common_denom = n_div * mod_div

        if common_denom == 1:
            remainder_to_r_options = {
                1: r_options
            }
            remainder_to_rem_options = {
                1: rem_options
            }
        else:
            n //= n_div
            mod //= mod_div

            remainder_to_r_options = collections.defaultdict(set)
            for r in r_options:
                remainder_to_r_options[r % common_denom].add(r % mod)

            remainder_to_rem_options = collections.defaultdict(set)
            for rem in rem_options:
                remainder_to_rem_options[rem % common_denom].add(rem % n)

            # Eagerly release rem_options in case of exponential blowup
            # to save memory
            del rem_options

        next_n = n*mod
        mod_inv = mod_mult_inv(mod, n)
        n_inv = mod_mult_inv(n, mod)
        # Given two congruences: (x % mod == a) and (x % q == b)
        # If mod and q are coprime then multiplicative inverses exist such that
        # mod*mod_inv % q == 1 and q*q_inv % mod == 1
        # We can construct the following
        # y = (a*q*q_inv + b*mod*mod_inv) % (mod*q)
        # Then y % mod == a and y % q == b. Thus y is a solution
        # We can then merge these into a "super congruence" and merge in the next one!

        rem_factor = mod*mod_inv
        r_factor = n*n_inv

        # Make sure to match up remainder options based on their remainder
        # mod common_denom. If their remainder mod common_denom do not match
        # then they imply *different* answers!
        for val, r_options in remainder_to_r_options.items():
            rem_options = remainder_to_rem_options.pop(val, None)
            if rem_options is None:
                continue

            for rem in rem_options:
                for r in r_options:
                    new_options.add((rem*rem_factor + r*r_factor) % next_n)

        n = next_n
        rem_options = new_options

        if len(rem_options) == 0:
            return None

    return min(rem_options)

def offset_chinese_remainder_incongruence(incongruencies):
    '''Efficiently calculates and returns the smallest number which works for
    all given *offset* incongruences. For example, given the following:
    (x + 0) % 4 != 0
    (x + 1) % 2 != 0
    (x + 4) % 6 != 0
    (x + 6) % 6 != 0
    The smallest x which satisfies all three is 10.
    If no solution exists, returns None.

    Arguments:
    incongruencies -- The list of incongruencies to use. Expected to be a list
    of (mod, offset) tuples.
    '''
    # Convert congruencies to chinese remainder form
    incongruencies = [(mod, (mod - (offset % mod)) % mod)
                      for mod, offset
                      in incongruencies]
    return chinese_remainder_incongruence(incongruencies)

def find_continuous_curve_minimum(domain, fn):
    '''Efficiently finds the input in the domain that minimizes the function
    value using pseudo-binary search. Only works for functions which are
    continuous and concave (that is, it has one local minimum which is the
    global minimum). For example, given the following function and domain:
    def sample_fn(x):
        return (x / 1000 - 5) ** 2
    domain = range(-10000000, 10000001)

    Using min(domain, key=sample_fn) will find 5000 as the answer, but it
    takes a few seconds to run since it has to call sample_fn for every input
    in the domain. (This can easily grow for larger domains or more expensive
    functions.) find_continuous_curve_minimum(domain, sample_fn) will return
    5000 nearly instantly as it only has to check a handful of points on the
    curve to find the global minimum.

    Arguments:
    domain -- A list-like sequence (supporting len and __getindex__) of inputs
    to test
    fn -- The continuous concave function. (If you want to find the maximum,
    just negate the output!)
    '''
    fn = functools.cache(fn)

    # Search through indices in the domain instead of the domain directly
    # This greatly accelerates the search when domain is a list since list
    # slices create copies rather than views into the list
    domain_indices = range(len(domain))

    pivot_idx = len(domain_indices)//2
    pivot = fn(domain[domain_indices[pivot_idx]])

    while len(domain_indices) > 4:
        low = domain_indices[:pivot_idx+1]
        high = domain_indices[pivot_idx:]

        low_side = len(low) > len(high)
        to_check = low if low_side else high

        check_idx = len(to_check)//2
        check_val = fn(domain[to_check[check_idx]])

        if check_val < pivot:
            # The check block is smaller than the entire other side, that means
            # that the minimum must lie inside the check block
            domain_indices = to_check
            pivot_idx = check_idx
            pivot = check_val
        else:
            # pivot is smaller, subdivide the big range accordingly
            if low_side:
                # The low side of the check block does not contain the minimum
                domain_indices = domain_indices[check_idx:]
                pivot_idx -= check_idx
                low = check_val
            else:
                # The high side of the check block does not contain the minimum
                domain_indices = domain_indices[:pivot_idx+check_idx+1]
                high = check_val

    min_idx = min(domain_indices, key=lambda idx:fn(domain[idx]))
    return domain[min_idx]

class Quadratic:
    '''Hold quadratic formula/functions and provides relevant operations/helpers
    to analyze and use them.
    '''
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __neg__(self):
        return Quadratic(-self.a,
                         -self.b,
                         -self.c)

    def __add__(self, other):
        assert(isinstance(other, Quadratic))
        return Quadratic(self.a + other.a,
                         self.b + other.b,
                         self.c + other.c)

    def __sub__(self, other):
        assert(isinstance(other, Quadratic))
        return Quadratic(self.a - other.a,
                         self.b - other.b,
                         self.c - other.c)

    def __call__(self, x):
        return x*x*self.a + x*self.b + self.c

    @property
    def terms(self):
        return self.a, self.b, self.c

    def solutions(self):
        '''Generates all solutions for when this quadratic equals zero
        '''
        if self.a == 0:
            return

        discriminant = self.b**2 - 4*self.a*self.c
        root = discriminant ** 0.5

        yield (-self.b + root) / (2 * self.a)
        yield (-self.b - root) / (2 * self.a)

    def real_solutions(self):
        '''Generates all real solutions for when this quadratic equals zero
        '''
        for s in self.solutions():
            if isinstance(s, complex):
                continue
            yield s

    def integral_solutions(self):
        '''Generates all integral solutions for when this quadratic equals zero
        '''
        for s in self.real_solutions():
            if round(s) != s:
                continue
            yield s
