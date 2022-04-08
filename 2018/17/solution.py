import lib.aoc

NEW_STATE = 0
CHECK0_STATE = 1
CHECK1_STATE = 2
CHECK2_STATE = 3

def run_sim(s):
    clay = set()
    for line in s.splitlines():
        a, b = line.split(', ')
        pos = int(a[2:])
        rs, re = list(map(int, b[2:].split('..')))
        r = range(rs, re+1)

        if a[0] == 'x':
            for y in r:
                clay.add((pos, y))
        else:
            for x in r:
                clay.add((x, pos))

    min_y = min(y for x,y in clay)
    max_y = max(y for x,y in clay)

    has_water = set()
    supports = set(clay)

    stack = [(500, 0, NEW_STATE)]

    while stack:
        x, y, state = stack.pop(-1)

        if state == NEW_STATE:
            state = CHECK0_STATE
            if y > max_y:
                continue
            has_water.add((x, y))
            if (x, y) in supports:
                # Known still water
                continue

        if state == CHECK0_STATE:
            state = CHECK1_STATE
            if (x, y+1) not in supports:
                stack.append((x, y, state))
                stack.append((x, y+1, NEW_STATE))
                continue

        if state == CHECK1_STATE:
            state = CHECK2_STATE
            if (x, y+1) not in supports:
                continue

        row_supported = True

        left_x = x-1
        while (left_x, y) not in clay:
            has_water.add((left_x, y))
            if (left_x, y+1) not in supports:
                if (left_x, y+1) not in has_water:
                    # This hasn't been checked yet. Check if it's supported.
                    # If it is, we'll re-flood
                    stack.append((left_x, y, NEW_STATE))
                row_supported = False
                break
            left_x -= 1

        right_x = x+1
        while (right_x, y) not in clay:
            has_water.add((right_x, y))
            if (right_x, y+1) not in supports:
                if (right_x, y+1) not in has_water:
                    # This hasn't been checked yet. Check if it's supported.
                    # If it is, we'll re-flood
                    stack.append((right_x, y, NEW_STATE))
                row_supported = False
                break
            right_x += 1

        if row_supported:
            for x in range(left_x+1, right_x):
                supports.add((x, y))

    all_water = sum(1 for x,y in has_water
                    if y >= min_y)
    still_water = len(supports - clay)
    return all_water, still_water

def part1(s):
    answer, _ = run_sim(s)

    lib.aoc.give_answer(2018, 17, 1, answer)

def part2(s):
    _, answer = run_sim(s)

    lib.aoc.give_answer(2018, 17, 2, answer)

INPUT = lib.aoc.get_input(2018, 17)
part1(INPUT)
part2(INPUT)
