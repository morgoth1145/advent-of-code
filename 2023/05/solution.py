import lib.aoc

def parse_input(s):
    groups = s.split('\n\n')

    seeds = groups[0]
    rest = groups[1:]

    seeds = list(map(int, seeds.split()[1:]))

    maps = {}

    for mapping in rest:
        lines = mapping.splitlines()
        key = lines[0]
        vals = []
        for l in lines[1:]:
            vals.append(tuple(map(int, l.split())))

        key = key.split()[0]
        a, b = key.split('-to-')
        maps[a,b] = vals

    return seeds, maps

def find_sequence(maps, start_type, end_type):
    seq = [start_type]

    while start_type != end_type:
        next_type = None
        for a, b in maps:
            if a == start_type:
                assert(next_type is None)
                next_type = b
        assert(next_type is not None)
        seq.append(next_type)
        start_type = next_type

    return seq

def do_mapping(val, maps, seq):
    seq = seq[:]
    while len(seq) > 1:
        a = seq.pop(0)
        b = seq[0]
        mapping = maps[a,b]

        new_val = None

        for dst, src, size in mapping:
            if src <= val < src+size:
                assert(new_val is None)
                off = val - src
                new_val = dst + off

        if new_val is None:
            new_val = val

        val = new_val

    return val

def part1(s):
    seeds, maps = parse_input(s)

    seq = find_sequence(maps, 'seed', 'location')

    answer = min(do_mapping(val, maps, seq)
                 for val in seeds)

    lib.aoc.give_answer(2023, 5, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 5)
part1(INPUT)
part2(INPUT)
