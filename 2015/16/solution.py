import lib.aoc

def parse_input(s):
    for line in s.splitlines():
        _, n, a, ac, b, bc, c, cc = line.split()

        left, right = line.split(': ', maxsplit=1)
        _, n = left.split()
        n = int(n)

        bits = []
        for thing in right.split(', '):
            name, count = thing.split(': ')
            count = int(count)
            bits.append((name, count))

        yield n, bits


def part1(s):
    for sue, bits in parse_input(s):
        bits = dict(bits)

        matches = True
        for key, expected in [('children', 3),
                              ('cats', 7),
                              ('samoyeds', 2),
                              ('pomeranians', 3),
                              ('akitas', 0),
                              ('vizslas', 0),
                              ('goldfish', 5),
                              ('trees', 3),
                              ('cars', 2),
                              ('perfumes', 1)]:
            if bits.get(key, expected) != expected:
                matches = False
                break

        if matches:
            answer = sue
            break

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 16)
part1(INPUT)
part2(INPUT)
