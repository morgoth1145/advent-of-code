import lib.aoc

def step(plant_offsets, plant_patterns):
    new_offsets = []

    for off in range(plant_offsets[0]-2, plant_offsets[-1]+3):
        key = []
        for i in range(off-2, off+3):
            key.append('#' if i in plant_offsets else '.')
        key = ''.join(key)

        if key in plant_patterns:
            new_offsets.append(off)

    adjust = new_offsets[0]
    plant_offsets = tuple(o-adjust
                          for o in new_offsets)

    return adjust, plant_offsets

def run(s, generations):
    groups = s.split('\n\n')

    start = groups[0].split()[2]

    plant_offsets = []
    for idx, c in enumerate(start):
        if c == '#':
            plant_offsets.append(idx)

    start = plant_offsets[0]
    plant_offsets = tuple(o-start
                          for o in plant_offsets)

    plant_patterns = set()

    for line in groups[1].splitlines():
        a, b = line.split(' => ')
        if b == '#':
            plant_patterns.add(a)

    assert('.....' not in plant_patterns)

    memory = {}
    sequence = []

    gen_num = 0
    while gen_num < generations:
        sequence.append((start, plant_offsets))
        if plant_offsets in memory:
            gen_seen, prev_start = memory[plant_offsets]
            # Jump ahead!

            repeat_every = gen_num - gen_seen
            shift_per = start - prev_start

            remaining = generations - gen_num
            jump_by = remaining // repeat_every
            gen_num += jump_by * repeat_every
            start += jump_by * shift_per
            break

        memory[plant_offsets] = (gen_num, start)
        gen_num += 1

        adjust, plant_offsets = step(plant_offsets, plant_patterns)
        start += adjust

    # Wrap up if needed
    while gen_num < generations:
        gen_num += 1
        adjust, plant_offsets = step(plant_offsets, plant_patterns)
        start += adjust

    return [o+start
            for o in plant_offsets]

def part1(s):
    answer = sum(run(s, 20))

    print(f'The answer to part one is {answer}')

def part2(s):
    answer = sum(run(s, 50000000000))

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 12)
part1(INPUT)
part2(INPUT)
