import lib.aoc

def parse_input(s):
    groups = s.split('\n\n')

    start = groups[0].split()[2]

    plants = set()
    for idx, c in enumerate(start):
        if c == '#':
            plants.add(idx)

    generate_plants = set()

    for line in groups[1].splitlines():
        a, b = line.split(' => ')
        if b == '#':
            generate_plants.add(a)

    assert('.....' not in generate_plants)

    return plants, generate_plants

def step(plants, generate_plants):
    out_plants = set()

    for idx in range(min(plants)-2, max(plants)+3):
        key = []
        for i in range(idx-2, idx+3):
            if i in plants:
                key.append('#')
            else:
                key.append('.')
        key = ''.join(key)
        if key in generate_plants:
            out_plants.add(idx)

    return out_plants

def part1(s):
    plants, generate_plants = parse_input(s)

    for _ in range(20):
        plants = step(plants, generate_plants)

    answer = sum(plants)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 12)
part1(INPUT)
part2(INPUT)
