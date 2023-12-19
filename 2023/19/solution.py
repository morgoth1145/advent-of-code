import collections
import json

import lib.aoc

Part = collections.namedtuple('Part',
                              ('x', 'm', 'a', 's'))

class Rule:
    def __init__(self, r):
        if ':' in r:
            self.const = False

            pred, self.dest = r.split(':')

            self._var = pred[0]
            op = pred[1]
            val = int(pred[2:])
            self._val = val

            if op == '<':
                self._test = lambda n: n < val
                self._filter_good = lambda vals: vals[:vals.index(val)]
                self._filter_bad = lambda vals: vals[vals.index(val):]
            elif op == '>':
                self._test = lambda n: n > val
                self._filter_good = lambda vals: vals[vals.index(val)+1:]
                self._filter_bad = lambda vals: vals[:vals.index(val)+1]
            else:
                assert(False)
        else:
            self.const = True
            self.dest = r

    def test(self, p):
        return self.const or self._test(getattr(p, self._var))

    def filter(self, p):
        if self.const:
            return p, None

        vals = getattr(p, self._var)
        if self._val in vals:
            good = p._replace(**{self._var:self._filter_good(vals)})
            bad = p._replace(**{self._var:self._filter_bad(vals)})
            return good, bad
        elif len(vals) > 0:
            if self._test(vals[0]):
                return p, p._replace(**{self._var:range(0)})
            else:
                return p._replace(**{self._var:range(0)}), p
        else:
            return p, p

def parse_input(s):
    a, b = s.split('\n\n')

    a = a.replace('{', ' ').replace('}', '')

    workflows = {}
    for line in a.splitlines():
        name, rules = line.split()
        workflows[name] = list(map(Rule, rules.split(',')))

    for c in 'xmas':
        b = b.replace(f'{c}=', f'"{c}":')

    parts = (Part(**json.loads(line))
             for line in b.splitlines())

    return workflows, parts

def part1(s):
    workflows, parts = parse_input(s)

    def accepted(name, p):
        if name == 'A':
            return True
        if name == 'R':
            return False
        for r in workflows[name]:
            if r.test(p):
                return accepted(r.dest, p)

    answer = sum(map(sum, (p for p in parts if accepted('in', p))))

    lib.aoc.give_answer(2023, 19, 1, answer)

def part2(s):
    workflows, _ = parse_input(s)

    def count_accepted(name, p):
        if name == 'A':
            return len(p.x) * len(p.m) * len(p.a) * len(p.s)
        if name == 'R':
            return 0

        count = 0

        for r in workflows[name]:
            good, p = r.filter(p)
            if good is not None:
                count += count_accepted(r.dest, good)
            if p is None:
                break

        return count

    answer = count_accepted('in',
                            Part(range(1, 4001),
                                 range(1, 4001),
                                 range(1, 4001),
                                 range(1, 4001)))

    lib.aoc.give_answer(2023, 19, 2, answer)

INPUT = lib.aoc.get_input(2023, 19)
part1(INPUT)
part2(INPUT)
