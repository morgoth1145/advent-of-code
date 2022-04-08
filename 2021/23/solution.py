import lib.aoc
import lib.graph

def solve(s):
    AMIPHIPODS = set()
    ROOM_X = set()
    WALLS = set()

    start = []
    grid = {}

    for y, row in enumerate(s.splitlines()):
        for x, c in enumerate(row):
            if c == '#':
                WALLS.add((x, y))
            elif c not in ' .':
                AMIPHIPODS.add(c)
                ROOM_X.add(x)
                start.append((c, (x, y)))

    AMIPHIPODS = ''.join(sorted(AMIPHIPODS))
    MOVE_COSTS = tuple(10 ** n for n in range(len(AMIPHIPODS)))
    ROOM_X = tuple(sorted(ROOM_X))
    start = tuple(sorted(start))

    ROOM_HEIGHT = len(start) // 4
    assert(len(start) == 4 * ROOM_HEIGHT)

    ROOM_Y = tuple(range(2, 2+ROOM_HEIGHT))

    end = []
    for x, c in zip(ROOM_X, AMIPHIPODS):
        for y in ROOM_Y:
            end.append((c, (x, y)))
    end = tuple(end)

    def neighbors(state):
        lookup = {pos:pod for pod, pos in state}

        def new_state(idx, pod, pos):
            new_state = state[:idx] + state[idx+1:]
            new_state += ((pod, pos),)
            return tuple(sorted(new_state))

        def is_free(x, y):
            return (x, y) not in lookup and (x, y) not in WALLS

        for idx, (pod, (x, y)) in enumerate(state):
            pod_idx = AMIPHIPODS.index(pod)

            moves = 0
            move_cost = MOVE_COSTS[pod_idx]
            target_x = ROOM_X[pod_idx]

            if y == 1:
                # It's in the hallway, it will only move into its room
                if any(lookup.get((target_x, ry), pod) != pod
                       for ry in ROOM_Y):
                    # It refuses to move when others are in the room!
                    continue

                dx = -1 if target_x < x else 1
                failed = False
                while x != target_x:
                    moves += 1
                    x += dx
                    if (x, y) in lookup:
                        # Can't pass whatever is here
                        failed = True
                        break

                if failed:
                    continue

                while is_free(x, y+1):
                    y += 1
                    moves += 1

                yield new_state(idx, pod, (x, y)), move_cost * moves
                continue

            # It must be in a room right now
            if x == target_x:
                # It's in it's target room!
                if all(lookup.get((x, oy), pod) == pod
                       for oy in ROOM_Y
                       if oy > y):
                    # There's no reason to leave, no amiphipod further in
                    # the room needs to leave!
                    continue

            failed = False
            while y > 1:
                moves += 1
                y -= 1
                if (x, y) in lookup:
                    # Can't pass whatever is here
                    failed = True
                    break

            if failed:
                continue

            # Try moving both ways
            for dx in (-1, 1):
                new_x = x
                new_moves = moves
                while is_free(new_x, y):
                    new_x += dx
                    new_moves += 1
                    if not is_free(new_x, y):
                        break
                    if new_x not in ROOM_X:
                        yield (new_state(idx, pod, (new_x, y)),
                               move_cost * new_moves)

    return lib.graph.dijkstra_length(lib.graph.make_lazy_graph(neighbors),
                                     start, end)

def part1(s):
    answer = solve(s)

    lib.aoc.give_answer(2021, 23, 1, answer)

def part2(s):
    lines = s.splitlines()
    lines = lines[:3] + [
        '  #D#C#B#A#',
        '  #D#B#A#C#'
        ] + lines[3:]
    s = '\n'.join(lines)

    answer = solve(s)

    lib.aoc.give_answer(2021, 23, 2, answer)

INPUT = lib.aoc.get_input(2021, 23)
part1(INPUT)
part2(INPUT)
