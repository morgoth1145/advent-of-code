import lib.aoc

def parse(s):
    for line in s.splitlines():
        inputs, outputs = line.split(' | ')
        yield inputs.split(), outputs.split()

def part1(s):
    answer = sum(len(pattern) in (2, 3, 4, 7)
                 for _, outputs in parse(s)
                 for pattern in outputs)

    print(f'The answer to part one is {answer}')

VALID_PATTERNS = {
    'abcefg':0,
    'cf':1,
    'acdeg':2,
    'acdfg':3,
    'bcdf':4,
    'abdfg':5,
    'abdefg':6,
    'acf':7,
    'abcdefg':8,
    'abcdfg':9
}

def map_display(m, n):
    new_n = ''.join(sorted(m[c] for c in n))
    return VALID_PATTERNS.get(new_n)

def find_output_number(line):
    patterns = sorted(line[0] + line[1], key=len)
    def do_search(m, patterns, unused_chars):
        if len(patterns) == 0:
            yield m
            return
        current = patterns[0]
        rest = patterns[1:]
        needed_chars = sorted(c for c in current if c not in m)
        if needed_chars:
            def iter_options(needed):
                if 0 == len(needed):
                    if map_display(m, current) is not None:
                        yield from do_search(m, rest, unused_chars)
                    return
                c = needed[0]
                rest_c = needed[1:]
                for t in list(unused_chars):
                    unused_chars.remove(t)
                    m[c] = t
                    yield from iter_options(rest_c)
                    del m[c]
                    unused_chars.add(t)
            yield from iter_options(needed_chars)
        elif map_display(m, current) is not None:
            yield from do_search(m, rest, unused_chars)

    mapping = next(do_search({}, patterns, set('abcdefg')))

    out = 0
    for n in line[1]:
        out = out * 10 + map_display(mapping, n)
    return out

def part2(s):
    answer = sum(map(find_output_number, parse(s)))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 8)
part1(INPUT)
part2(INPUT)
