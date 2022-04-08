import collections

import lib.aoc
import lib.cyk

def parse_input(s):
    g0, molecule = s.split('\n\n')

    rules = collections.defaultdict(list)
    for line in g0.splitlines():
        left, right = line.split(' => ')
        assert(len(left) <= len(right))
        rules[left].append(right)

    return rules, molecule

def part1(s):
    rules, molecule = parse_input(s)

    possibilities = set()

    for base, replacements in rules.items():
        last_idx = 0
        while True:
            idx = molecule.find(base, last_idx)
            if idx == -1:
                break
            for repl in replacements:
                new = molecule[:idx] + repl + molecule[idx+len(base):]
                possibilities.add(new)
            last_idx = idx + len(base)

    answer = len(possibilities)

    lib.aoc.give_answer(2015, 19, 1, answer)

def tokenize_by_element(molecule):
    # Weird special case...
    if molecule == 'e':
        return ['e']

    # All elements are camel case
    indices = [i for i,c in enumerate(molecule)
               if c.isupper()]
    assert(len(indices) > 0 and indices[0] == 0)
    return [molecule[i1:i2]
            for i1, i2 in zip(indices, indices[1:] + [len(molecule)])]

def to_grammar(rules):
    known_elements = set()

    for base, options in sorted(rules.items()):
        assert(len(tokenize_by_element(base)) == 1)
        known_elements.add(base)
        for opt in options:
            option_elements = tokenize_by_element(opt)
            known_elements.update(option_elements)
            yield lib.cyk.Symbol(base), list(map(lib.cyk.Symbol,
                                                 option_elements))

    for elem in known_elements:
        # Mark this free, we only use symbols for compatibility with lib.cyk!
        yield lib.cyk.Symbol(elem), elem, 0

def part2(s):
    rules, molecule = parse_input(s)

    cnf = lib.cyk.CNFGrammar(to_grammar(rules), lib.cyk.Symbol('e'))

    answer = cnf.steps_to_generate(tokenize_by_element(molecule))

    lib.aoc.give_answer(2015, 19, 2, answer)

INPUT = lib.aoc.get_input(2015, 19)
part1(INPUT)
part2(INPUT)
