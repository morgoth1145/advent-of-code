import lib.aoc

def solve(s):
    groups = s.split('\n\n')

    presents = []

    for g in groups[:-1]:
        lines = g.splitlines()
        idx = int(lines[0].split(':')[0])
        assert(idx == len(presents))

        pres_pattern = '\n'.join(lines[1:])

        width = len(lines[1])
        height = len(lines[1:])
        occupied = pres_pattern.count('#')

        presents.append((width, height, occupied, pres_pattern))

    pres_w = set(w for w,_,_,_ in presents)
    pres_h = set(h for _,h,_,_ in presents)

    assert(len(pres_w | pres_h) == 1)
    pres_dim = list(pres_w)[0]

    low_bound = 0
    high_bound = 0

    for line in groups[-1].splitlines():
        dim, counts = line.split(': ')
        width, height = map(int, dim.split('x'))
        counts = list(map(int, counts.split()))

        if sum(counts) <= (width // pres_dim) * (height // pres_dim):
            # Must fit if there are enough DIMxDIM areas in the region
            low_bound += 1
            high_bound += 1
            continue

        total_occupied = sum(c*o for c, (_,_,o,_) in zip(counts, presents))
        if total_occupied > width*height:
            # Cannot fit by pidgeonhole principle, there would be more occupied tiles than available in the region
            continue

        print(f'Region {width}x{height}: {counts} may be solvable, this code is not smart enough to check right now.')
        high_bound += 1

    print(f'{low_bound}-{high_bound} regions are satisfied')
    assert(low_bound == high_bound)

    return low_bound

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2025, 12, 1, answer)

def part2(s):
    print('There is no part 2 on day 12!')

INPUT = lib.aoc.get_input(2025, 12)
part1(INPUT)
part2(INPUT)
