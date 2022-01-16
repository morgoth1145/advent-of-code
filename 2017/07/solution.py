import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        bits = line.split(' -> ')
        a, b = bits[0].split()
        assert(b[0] == '(' and b[-1] == ')')
        b = int(b[1:-1])
        if len(bits) == 2:
            rest = bits[1].split(', ')
        else:
            rest = []
        yield a, b, rest

def part1(s):
    seen = set()
    referenced = set()

    for name, weight, held in parse_input(s):
        seen.add(name)
        referenced.update(held)

    base = list(seen - referenced)
    assert(len(base) == 1)

    answer = base[0]

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2017, 7)
part1(INPUT)
part2(INPUT)
