import collections
import typing

class IntegerDomain(typing.NamedTuple):
    low: int
    high: int

    def __add__(self, other):
        if isinstance(other, int):
            return IntegerDomain(self.low + other, self.high + other)
        if isinstance(other, IntegerDomain):
            return IntegerDomain(self.low + other.low, self.high + other.high)
        raise TypeError()

    def __mul__(self, other):
        if isinstance(other, int):
            a = self.low * other
            b = self.high * other
            return IntegerDomain(min(a, b), max(a, b))
        if isinstance(other, IntegerDomain):
            a = self.low * other.low
            b = self.low * other.high
            c = self.high * other.low
            d = self.high * other.high
            return IntegerDomain(min(a, b, c, d), max(a, b, c, d))
        raise TypeError()

    def __pow__(self, power):
        if isinstance(power, int):
            assert(power > 0)
            a = self.low ** power
            b = self.high ** power
            if power % 2 == 0 and 0 in self:
                return IntegerDomain(0, max(a, b))
            else:
                return IntegerDomain(a, b)
        raise TypeError()

    def __contains__(self, value):
        return self.low <= value <= self.high

    def __str__(self):
        return f'IntegerDomain({self.low}, {self.high})'

    def __repr__(self):
        return str(self)

class Symbol:
    def __init__(self, name, domain):
        assert(isinstance(domain, IntegerDomain))
        self.name = name
        self.domain = domain

    def _to_expression(self):
        return Expression([(1, [(self, 1)])])

    def __neg__(self):
        return -self._to_expression()

    def __add__(self, other):
        return self._to_expression() + other

    def __sub__(self, other):
        return self._to_expression() - other

    def __mul__(self, other):
        return self._to_expression() * other

    def __floordiv__(self, other):
        return self._to_expression() // other

    def __mod__(self, other):
        return self._to_expression() % other

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Symbol({str(self)})'

    def __lt__(self, other):
        return self.name < other.name

def _term_domain(term):
    factor, symbols = term

    domain = IntegerDomain(factor, factor)

    for s, power in symbols:
        domain *= s.domain ** power

    return domain

def _normalize_term(term):
    factor, symbols = term
    symbol_powers = collections.Counter()

    for s, power in symbols:
        symbol_powers[s] += power

    return factor, tuple(sorted((s, power)
                                for s, power in symbol_powers.items()
                                if power != 0))

class Expression:
    def __init__(self, terms=[]):
        term_factors = collections.Counter()

        for factor, symbols in map(_normalize_term, terms):
            term_factors[symbols] += factor

        self._terms = [(factor, symbols)
                       for symbols, factor in term_factors.items()
                       if factor != 0]

    def substitute(self, symbol_to_replace, value):
        new_terms = []

        for factor, symbols in self._terms:
            new_symbols = []

            for s, power in symbols:
                if s == symbol_to_replace:
                    factor *= value ** power
                else:
                    new_symbols.append((s, power))

            new_terms.append((factor, tuple(new_symbols)))

        return Expression(new_terms)

    def get_domain(self):
        domain = IntegerDomain(0, 0)

        for term in self._terms:
            domain += _term_domain(term)

        return domain

    def __neg__(self):
        return Expression([(-factor, symbols)
                           for factor, symbols in self._terms])

    def __add__(self, other):
        if isinstance(other, int):
            return Expression(self._terms + [(other, tuple())])
        if isinstance(other, Symbol):
            return Expression(self._terms + [(1, ((other, 1),))])
        if isinstance(other, Expression):
            return Expression(self._terms + other._terms)
        self._report_unsupported(other, 'add')

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        if isinstance(other, int):
            return Expression([(factor * other, symbols)
                               for factor, symbols in self._terms])
        if isinstance(other, Symbol):
            return Expression([(factor, symbols + ((other, 1),))
                               for factor, symbols in self._terms])
        if isinstance(other, Expression):
            other_domain = other.get_domain()
            if other_domain.low == other_domain.high:
                # It's a single value expression, we can multipliy
                return self * other_domain.low
        self._report_unsupported(other, 'mul')

    def __floordiv__(self, other):
        if isinstance(other, int):
            new_terms = []
            for factor, symbols in self._terms:
                if factor % other == 0:
                    # f * v // d is equivalent to (f // d) * v if
                    # f % d == 0
                    new_terms.append((factor // other, symbols))
                else:
                    term_domain = _term_domain((factor, symbols))
                    if term_domain.low == term_domain.high:
                        # It's a constant so just apply it
                        new_terms.append((term_domain.low // other, tuple()))
                    else:
                        if 0 <= term_domain.low and term_domain.high < other:
                            # This term disappears
                            continue
                        self._report_unsupported(other, 'floordiv (special int case)')
            return Expression(new_terms)
        self._report_unsupported(other, 'floordiv')

    def __mod__(self, other):
        if isinstance(other, int):
            new_terms = []
            for factor, symbols in self._terms:
                if factor % other == 0:
                    # This term cancels out!
                    continue

                term_domain = _term_domain((factor, symbols))
                if term_domain.low == term_domain.high:
                    # It's a constant so just apply it
                    new_terms.append((term_domain.low % other, tuple()))
                elif 0 <= term_domain.low and term_domain.high < other:
                    # This term remains as-is
                    new_terms.append((factor, symbols))
                else:
                    self._report_unsupported(other, 'mod (special int case)')
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
            term_parts += [f'({s.name} ** {power})' for s, power in symbols]
            parts.append('*'.join(term_parts))
        return ' + '.join(parts)

    def __repr__(self):
        return f'Expression({str(self)})'

    def _report_unsupported(self, other, op_type):
        print(f'Unsupported expression operation: {op_type} with {type(other)}')
        print(f'self: {self}')
        print(f'other: {other}')
        assert(False)

def Constant(value):
    return Expression([(value, tuple())])

class Equality:
    def __init__(self, left, right):
        self.expr = left - right
        self.expr_domain = self.expr.get_domain()

    @property
    def satisfiable(self):
        return 0 in self.expr_domain

    @property
    def forced(self):
        return self.expr_domain.low == 0 == self.expr_domain.high

    def substitute(self, symbol_to_replace, value):
        return Equality(self.expr.substitute(symbol_to_replace, value), 0)

    def __repr__(self):
        return f'Equality({self.expr}, 0)'

class Inequality:
    def __init__(self, left, right):
        self.expr = left - right
        self.expr_domain = self.expr.get_domain()

    @property
    def satisfiable(self):
        return self.expr_domain.low != 0 or self.expr_domain.high != 0

    @property
    def forced(self):
        return self.expr_domain.low > 0 or self.expr_domain.high < 0

    def substitute(self, symbol_to_replace, value):
        return Inequality(self.expr.substitute(symbol_to_replace, value), 0)

    def __repr__(self):
        return f'Inequality({self.expr}, 0)'
