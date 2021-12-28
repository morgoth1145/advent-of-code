import lib.aoc

def decode(line):
    assert(line[0] == '"' == line[-1])
    line = line[1:-1]

    out = []

    idx = 0
    while idx < len(line):
        c = line[idx]
        idx += 1

        if c != '\\':
            out.append(c)
            continue

        nc = line[idx]
        idx += 1
        if nc in '"\\':
            out.append(nc)
            continue

        assert(nc == 'x')
        code = line[idx:idx+2]
        idx += 2
        c = ascii(int(code, 16))
        out.append('#') # PLACEHOLDER FOR PART 1

    return ''.join(out)

def part1(s):
    lines = s.splitlines()
    answer = sum(map(len, lines)) - sum(map(len, map(decode, lines)))

    print(f'The answer to part one is {answer}')

def encode(line):
    out = []

    for c in line:
        if c in '"\\':
            out.append('\\')
        out.append(c)

    return '"' + ''.join(out) + '"'

def part2(s):
    lines = s.splitlines()
    answer = sum(map(len, map(encode, lines))) - sum(map(len, lines))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 8)
part1(INPUT)
part2(INPUT)
