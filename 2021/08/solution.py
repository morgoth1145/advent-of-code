import lib.aoc

def parse(s):
    for line in s.splitlines():
        start, end = line.split(' | ')
        start = [''.join(sorted(set(i))) for i in start.split()]
        end = [''.join(sorted(set(o))) for o in end.split()]
        yield start, end

def part1(s):
    answer = 0
    for _, outputs in parse(s):
        for pattern in outputs:
            if len(pattern) in (2, 3, 4, 7):
                answer += 1

    print(f'The answer to part one is {answer}')

VALID_PATTERNS = [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg'
]
VALID_PATTERNS = {
    p:idx for idx,p in enumerate(VALID_PATTERNS)
}

KNOWN_LENGTHS = {
    2: 1,
    3: 7,
    4: 4,
    7: 8
}

def map_display(m, n):
    return VALID_PATTERNS.get(''.join(sorted(m[c] for c in n)))

def determine_mapping(line):
    patterns = line[0] + line[1]
    patterns = sorted(patterns, key=len)
    def do_search(m, patterns, unused_chars):
        if len(patterns) == 0:
            yield m
            return
        current = patterns[0]
        rest = patterns[1:]
        needed_chars = [c for c in current if c not in m]
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
    return next(do_search({}, patterns, set('abcdefg')))

def figure_number(mapping, ending):
    out = 0
    for n in ending:
        out *= 10
        out += VALID_PATTERNS[''.join(sorted(mapping[c] for c in n))]
    return out

def part2(s):
    answer = 0
    for line in parse(s):
        m = determine_mapping(line)
        n = figure_number(m, line[1])
        answer += n

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2021, 8)
part1(INPUT)
part2(INPUT)
