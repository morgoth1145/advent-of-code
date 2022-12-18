import lib.aoc

def parse_lava(s):
    return set(tuple(map(int, line.split(',')))
               for line in s.splitlines())

def neighbors(x, y, z):
    return {(x-1, y, z), (x+1, y, z),
            (x, y-1, z), (x, y+1, z),
            (x, y, z-1), (x, y, z+1)}

def part1(s):
    lava = parse_lava(s)

    answer = sum(len(neighbors(x, y, z) - lava)
                 for x, y, z in lava)

    lib.aoc.give_answer(2022, 18, 1, answer)

def part2(s):
    lava = parse_lava(s)

    min_x = min(x for x,y,z in lava)
    max_x = max(x for x,y,z in lava)
    min_y = min(y for x,y,z in lava)
    max_y = max(y for x,y,z in lava)
    min_z = min(z for x,y,z in lava)
    max_z = max(z for x,y,z in lava)

    x_range = range(min_x-1, max_x+2)
    y_range = range(min_y-1, max_y+2)
    z_range = range(min_z-1, max_z+2)

    outside_air = {(min_x-1, min_y-1, min_z-1)}
    to_handle = [(min_x-1, min_y-1, min_z-1)]

    # Flood fill the exterior to find which voxels are air
    while to_handle:
        x, y, z = to_handle.pop()
        if x not in x_range or y not in y_range or z not in z_range:
            continue
        newly_found_air = neighbors(x, y, z) - outside_air - lava
        outside_air.update(newly_found_air)
        to_handle.extend(newly_found_air)

    answer = sum(len((neighbors(x, y, z) & outside_air) - lava)
                 for x, y, z in lava)

    lib.aoc.give_answer(2022, 18, 2, answer)

INPUT = lib.aoc.get_input(2022, 18)
part1(INPUT)
part2(INPUT)
