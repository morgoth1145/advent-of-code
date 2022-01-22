import lib.aoc

def sequence_generator(val, fact, mod):
    while True:
        val = (val * fact) % mod
        yield val

def parse_sequences(s):
    a, b = s.splitlines()
    a = int(a.split()[-1])
    b = int(b.split()[-1])

    MOD = 2147483647

    return sequence_generator(a, 16807, MOD), sequence_generator(b, 48271, MOD)

def judge(a, b, to_check):
    BIT_MASK = 0xFFFF # 16 bits

    matched = 0

    for _ in range(to_check):
        if next(a) & BIT_MASK == next(b) & BIT_MASK:
            matched += 1

    return matched

def part1(s):
    a, b = parse_sequences(s)
    answer = judge(a, b, 40000000)

    print(f'The answer to part one is {answer}')

def part2(s):
    a, b = parse_sequences(s)

    a = filter(lambda val: val % 4 == 0, a)
    b = filter(lambda val: val % 8 == 0, b)

    answer = judge(a, b, 5000000)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 15)
part1(INPUT)
part2(INPUT)
