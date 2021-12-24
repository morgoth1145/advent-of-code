import collections
import itertools

class Symbol:
    def __init__(self, name, options):
        self.name = name
        self.options = options

    def __neg__(self):
        # Needed for Expression() - Symbol()!
        return Expression([(-1, [self])])

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Symbol({str(self)})'

def _symbol_prod_options(symbols):
    options = {1}
    for s in symbols:
        options = {o0 * o1
                   for o0 in options
                   for o1 in s.options}
    return options

def _simplify_terms(terms):
    new_term_factors = collections.Counter()
    for factor, symbols in terms:
        symbols = tuple(sorted(symbols, key=lambda s: s.name))
        new_term_factors[symbols] += factor

    return [(factor, symbols)
            for symbols, factor in new_term_factors.items()
            if factor != 0]

def _get_term_options(terms):
    options = {0}
    for factor, symbols in terms:
        options = {factor * sprod_val
                   for sprod_val in _symbol_prod_options(symbols)}
    return options

class Expression:
    def __init__(self, terms=[]):
        self._terms = _simplify_terms(terms)

    def gen_substitutions(self):
        '''Generates all symbol substitutions and their results'''

        all_symbols = list(set(s
                               for _, symbols in self._terms
                               for s in symbols))
        symbol_lookup = {s: idx
                         for idx, s in enumerate(all_symbols)}

        symbol_option_list = [s.options for s in all_symbols]

        for substitution in itertools.product(*symbol_option_list):
            result = 0
            for factor, symbols in self._terms:
                t = factor
                for s in symbols:
                    t *= substitution[symbol_lookup[s]]
                result += t
            yield result, tuple(zip(all_symbols, substitution))

    def __neg__(self):
        return Expression([(-factor, symbols)
                           for factor, symbols in self._terms])

    def __add__(self, other):
        if isinstance(other, int):
            return Expression(self._terms + [(other, tuple())])
        if isinstance(other, Symbol):
            return Expression(self._terms + [(1, (other,))])
        if isinstance(other, Expression):
            return Expression(self._terms + other._terms)
        self._report_unsupported(other, 'add')

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        if isinstance(other, int):
            return Expression([(factor * other, symbols)
                               for factor, symbols in self._terms])
        if isinstance(other, Expression):
            val_options = list(_get_term_options(other._terms))
            if len(val_options) == 1:
                return self * val_options[0]
        self._report_unsupported(other, 'mul')

    def __floordiv__(self, other):
        if isinstance(other, int):
            new_terms = []
            for factor, symbols in self._terms:
                if factor % other == 0:
                    # f * v // d is equivalent to (f // d) * v if
                    # f % d == 0
                    new_terms.append((factor // other, symbols))
                elif 0 == len(symbols):
                    # There are no symbols, so just apply it!
                    new_terms.append((factor // other, symbols))
                else:
                    if all(0 <= factor * v < other
                           for v in _symbol_prod_options(symbols)):
                        # This term disappears!
                        continue
                    self._report_unsupported(other, 'floordiv (special int case)')
            return Expression(new_terms)
        self._report_unsupported(other, 'floordiv')

    def __mod__(self, other):
        if isinstance(other, int):
            # f * v % m is equivalent to (f % m) * v so long as
            # v % m == v for all possible v
            new_terms = []
            for factor, symbols in self._terms:
                if not all(0 <= v < other
                           for v in _symbol_prod_options(symbols)):
                    # Our precondition is violated!
                    self._report_unsupported(other,
                                             'mod (special int case)')
                new_terms.append((factor % other, symbols))
            return Expression(new_terms)
        self._report_unsupported(other, 'mod')

    def __str__(self):
        if 0 == len(self._terms):
            return '0'
        parts = []
        for factor, symbols in self._terms:
            term_parts = []
            if factor != 1 or 0 == len(symbols):
                term_parts.append(str(factor))
            term_parts += [s.name for s in symbols]
            parts.append('*'.join(term_parts))
        return ' + '.join(parts)

    def __repr__(self):
        return f'Expression({str(self)})'

    def _report_unsupported(self, other, op_type):
        print(f'Unsupported expression operation: {op_type} with {type(other)}')
        print(f'self: {self}')
        print(f'other: {other}')
        assert(False)
