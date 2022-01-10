import collections
import functools
import itertools

class Symbol:
    def __init__(self, identifier):
        self.id = identifier

    def __str__(self):
        return f'Symbol({self.id})'

    def __repr__(self):
        return str(self)

def _PARSE_RULE(rule):
    if 2 == len(rule):
        lhs, rhs = rule
        steps = 1
    else:
        lhs, rhs, steps = rule

    assert(isinstance(lhs, Symbol))
    assert(isinstance(lhs.id, str))

    if rhs == '':
        rhs = tuple()

    if isinstance(rhs, str):
        rhs = (rhs,)

    rhs = tuple(rhs)
    assert(all(((isinstance(term, Symbol) and isinstance(term.id, str)) or
                isinstance(term, str))
               for term in rhs))

    return lhs, rhs, steps

def _RUN_TERM(rules, symbol_num_counter):
    term_str_to_num = {}

    for lhs, options in rules.items():
        new_options = []
        for rhs, steps in options:
            new_rhs = []
            for term in rhs:
                if isinstance(term, str):
                    terminal_num = term_str_to_num.get(term)
                    if terminal_num is None:
                        terminal_num = next(symbol_num_counter)
                        term_str_to_num[term] = terminal_num
                    new_rhs.append(terminal_num)
                else:
                    new_rhs.append(term)
            new_options.append((tuple(new_rhs), steps))
        rules[lhs] = new_options

    for term, terminal_num in term_str_to_num.items():
        rules[terminal_num] = [(term, 0)]

    return rules

def _RUN_BIN(rules, symbol_num_counter):
    new_rules = collections.defaultdict(set)
    for lhs, options in rules.items():
        for rhs, steps in options:
            if isinstance(rhs, str):
                new_rules[lhs].add((rhs, steps))
                continue
            target_lhs = lhs
            while len(rhs) > 2:
                new_symbol = next(symbol_num_counter)
                new_rules[target_lhs].add(((rhs[0], new_symbol), 0))
                target_lhs = new_symbol
                rhs = rhs[1:]
            new_rules[target_lhs].add((rhs, steps))

    return new_rules

def _RUN_DEL(rules, start):
    steps_to_null = {}

    while True:
        new_nullables = []

        for lhs, options in rules.items():
            new_options = []
            for rhs, steps in options:
                if rhs == tuple():
                    # Nullable!
                    new_nullables.append(lhs)
                    steps_to_null[lhs] = min(steps,
                                             steps_to_null.get(lhs, steps))
                else:
                    new_options.append((rhs, steps))
            rules[lhs] = new_options

        if len(new_nullables) == 0:
            # No nullable rules remain
            return rules, steps_to_null.get(start)

        new_rules = {}
        for lhs, options in rules.items():
            new_options = {}
            for rhs, steps in options:
                if isinstance(rhs, str):
                    new_options[rhs] = min(steps, new_options.get(rhs, steps))
                    continue

                positions = [idx for idx, part in enumerate(rhs)
                             if part in steps_to_null]

                for num_to_remove in range(0, len(positions)+1):
                    for to_remove in itertools.combinations(positions,
                                                            num_to_remove):
                        extra_steps = sum(steps_to_null[rhs[idx]]
                                          for idx in to_remove)
                        new_steps = steps + extra_steps
                        new_rhs = tuple(part for idx, part in enumerate(rhs)
                                        if idx not in to_remove)
                        if new_rhs == tuple():
                            known_steps = steps_to_null.get(lhs)
                            if known_steps is not None and known_steps <= new_steps:
                                # We're inlining this epsilon at this steps already!
                                continue
                        new_options[new_rhs] = min(new_steps,
                                                   new_options.get(new_rhs,
                                                                   new_steps))
            new_rules[lhs] = list(new_options.items())

        rules = new_rules

def _RUN_UNIT(rules, start):
    while True:
        improved = False
        for lhs, options in rules.items():
            for rhs, steps in options:
                if isinstance(rhs, tuple) and len(rhs) == 1:
                    new_options = {}
                    for o, c in options:
                        if o == rhs:
                            continue
                        new_options[o] = c
                    if rhs[0] != lhs:
                        for o, s in rules.get(rhs[0], []):
                            new_steps = steps + s
                            # Take the minimum steps on duplicates
                            new_options[o] = min(new_steps,
                                                 new_options.get(o, new_steps))
                    rules[lhs] = list(new_options.items())
                    improved = True
                    break
        if not improved:
            return rules

def _RUN_PRUNE_UNREFERENCED(rules, start):
    referenced = set()
    to_process = [start]
    while to_process:
        item = to_process.pop()
        if item in referenced:
            continue
        referenced.add(item)
        for rhs, steps in rules.get(item, []):
            if isinstance(rhs, str):
                continue
            to_process.extend(rhs)

    for unreferenced in set(rules.keys()) - referenced:
        del rules[unreferenced]

    return rules

def _RUN_PRUNE_NONTERMINAL(rules, start):
    can_terminate = set()
    for lhs, options in rules.items():
        if any(isinstance(rhs, str)
               for rhs, steps in options):
            can_terminate.add(lhs)

    while True:
        expanded = False
        for lhs, options in rules.items():
            if lhs in can_terminate:
                continue

            for rhs, steps in options:
                if isinstance(rhs, str):
                    continue
                if any(item in can_terminate
                       for item in rhs):
                    can_terminate.add(lhs)
                    expanded = True
                    break

        if not expanded:
            break

    for lhs in set(rules.keys()) - can_terminate:
        del rules[lhs]

    for lhs, options in rules.items():
        new_options = []
        for rhs, steps in options:
            if isinstance(rhs, str):
                new_options.append((rhs, steps))
            elif all(item in can_terminate
                     for item in rhs):
                new_options.append((rhs, steps))
        rules[lhs] = new_options

    return rules

def _RUN_COMPRESS_NUMBERING(rules, start):
    renumbering = {}
    for n in sorted(rules.keys()):
        renumbering[n] = len(renumbering)

    rules = {
        renumbering[n]: [(rhs if isinstance(rhs, str)
                          else tuple(renumbering[term] for term in rhs),
                          steps)
                          for rhs, steps in options]
        for n, options in rules.items()
    }
    return rules, renumbering[start]

class CNFGrammar:
    '''
    Holds onto Chomsky normal form grammars. Accepts valid context-free grammars
    and converts them to Chomsky normal form.

    Provides helpers for checking whether messages match the grammar as well
    as counting how many steps it takes to generate a message with the grammar.

    https://en.wikipedia.org/wiki/Chomsky_normal_form
    '''
    def __init__(self, rules, start):
        '''
        Arguments:
        rules -- Sequence of tuples (left, right, [steps=1])
        left must be a lib.cyk.Symbol
        right may be a single string or a sequence of lib.cyk.Symbol and/or strings
        If present steps overrides how many steps a given rule "costs"

        start -- lib.cyk.Symbol

        Strings are accepted as-is. It is expected that downstream matching will
        occur on pre-tokenized messages. Furthermore, the start symbol *must*
        appear at least once on the left hand side of a rule.
        '''
        assert(isinstance(start, Symbol))

        rule_list = list(map(_PARSE_RULE, rules))

        assert(any(lhs.id == start.id
                   for lhs, _, _ in rule_list))

        symbol_num_counter = itertools.count()

        symbol_to_num = {start.id: next(symbol_num_counter)}

        for lhs, _, _ in rule_list:
            num = symbol_to_num.get(lhs.id)
            if num is None:
                symbol_to_num[lhs.id] = next(symbol_num_counter)

        start = symbol_to_num[start.id]
        rules = collections.defaultdict(list)
        for lhs, rhs, steps in rule_list:
            lhs = symbol_to_num[lhs.id]
            rhs = tuple(symbol_to_num.get(term.id)
                        if isinstance(term, Symbol)
                        else term
                        for term in rhs)
            if None in rhs:
                # Invalid rule, this can't be expanded!
                continue
            if rhs == (lhs,):
                # Don't allow self-identity rules. That's silly.
                continue
            rules[lhs].append((rhs, steps))

        # TERM: Eliminate rules with nonsolitary terminals
        rules = _RUN_TERM(rules, symbol_num_counter)

        # BIN: Eliminate right hand sides with more than 2 nonterminals
        rules = _RUN_BIN(rules, symbol_num_counter)

        # DEL: Eliminate epsilon rules
        rules, steps_to_null = _RUN_DEL(rules, start)

        # UNIT: Eliminate unit rules
        rules = _RUN_UNIT(rules, start)

        rules = _RUN_PRUNE_UNREFERENCED(rules, start)

        rules = _RUN_PRUNE_NONTERMINAL(rules, start)

        # Not strictly needed, but it is kind of nice to have compressed rules
        rules, start = _RUN_COMPRESS_NUMBERING(rules, start)

        self.__start = start
        self.__steps_to_null = steps_to_null

        self.__term_to_symbol_steps = collections.defaultdict(list)
        self.__symbol_pair_to_source_steps = collections.defaultdict(list)
        symbol_pair_to_source = collections.defaultdict(list)

        for lhs, options in rules.items():
            for rhs, steps in options:
                if isinstance(rhs, str):
                    self.__term_to_symbol_steps[rhs].append((lhs, steps))
                else:
                    self.__symbol_pair_to_source_steps[rhs].append((lhs, steps))
                    symbol_pair_to_source[rhs].append(lhs)

        self.__term_to_symbol_steps = {key: tuple(sorted(value))
                                       for key, value
                                       in self.__term_to_symbol_steps.items()}

        self.__symbol_pair_to_source_steps = {key: tuple(sorted(value))
                                              for key, value
                                              in self.__symbol_pair_to_source_steps.items()}

        symbol_pair_to_source = {key: tuple(sorted(value))
                                 for key, value
                                 in symbol_pair_to_source.items()}

        # Prepared for the matches method. Typically faster since many
        # left_cands, right_cands pairs are seen repeatedly when processing
        # messages. I've seen anywhere from a 2x speedup for normal grammars
        # to massive 30-50x speedups for degenerate grammars.
        @functools.cache
        def sources_to_generate_span(left_cands, right_cands):
            return tuple(set(filter(None,
                                    map(symbol_pair_to_source.get,
                                        itertools.product(left_cands,
                                                          right_cands)))))
        self.__sources_to_generate_span = sources_to_generate_span

    def matches(self, message):
        # https://en.wikipedia.org/wiki/CYK_algorithm
        if len(message) == 0:
            return self.__steps_to_null is not None

        P = [[tuple()] * (len(message)-i+1+1) for i in range(len(message)+1)]
        for idx, term in enumerate(message):
            s = idx+1
            symbol_steps = self.__term_to_symbol_steps.get(term)
            if symbol_steps is None:
                return False
            P[1][s] = tuple(s for s, steps in symbol_steps)

        for l in range(2, len(message)+1): # Length of span
            for s in range(1, len(message)-l+2): # Start of span
                source_lists = [self.__sources_to_generate_span(P[p][s],
                                                                P[l-p][s+p])
                                for p in range(1, l) # Partition of span
                                ]

                new_symbols = set()
                list(map(new_symbols.update,
                         itertools.chain(*source_lists)))
                P[l][s] = tuple(sorted(new_symbols))

        return self.__start in P[len(message)][1]

    def steps_to_generate(self, message):
        # https://en.wikipedia.org/wiki/CYK_algorithm
        # Modified to keep track of the steps to generate the message
        if len(message) == 0:
            return self.__steps_to_null

        P = [[tuple()] * (len(message)-i+1+1) for i in range(len(message)+1)]
        for idx, term in enumerate(message):
            s = idx+1
            symbol_steps = self.__term_to_symbol_steps.get(term)
            if symbol_steps is None:
                return False
            P[1][s] = symbol_steps

        for l in range(2, len(message)+1): # Length of span
            for s in range(1, len(message)-l+2): # Start of span
                new_steps = {}
                for p in range(1, l): # Partition of span
                    for (l_s, l_steps), (r_s, r_steps) in itertools.product(P[p][s],
                                                                            P[l-p][s+p]):
                        symbol_steps = self.__symbol_pair_to_source_steps.get((l_s, r_s))
                        if symbol_steps is None:
                            continue
                        for sym, steps in symbol_steps:
                            steps = l_steps + r_steps + steps
                            new_steps[sym] = min(new_steps.get(sym, steps), steps)
                P[l][s] = tuple(new_steps.items())

        for s, steps in P[len(message)][1]:
            if s == self.__start:
                return steps

        return None
