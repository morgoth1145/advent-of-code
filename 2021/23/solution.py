import lib.aoc
import lib.graph
import lib.grid

def part1(s):
    lines = s.splitlines()
    target_len = max(map(len, lines))
    lines = [l + ' ' * (target_len - len(l))
             for l in lines]
    s = '\n'.join(lines)
    grid = lib.grid.FixedGrid.parse(s)

    OUTSIDE_ROOM = [(3,1), (5,1), (7,1), (9,1)]

    ROOMS = [(3,2), (5,2), (7,2), (9,2),
             (3,3), (5,3), (7,3), (9,3)]
    ROOM_TO_BASE = {
        (3,2): (3,3),
        (5,2): (5,3),
        (7,2): (7,3),
        (9,2): (9,3),
    }

    TARGET = 'ABCDABCD'
    CURRENT = ''.join(grid[c] for c in ROOMS)

    START = [(CURRENT[i], ROOMS[i])
             for i in range(len(ROOMS))]
    START_ROOMS = tuple(sorted(START))
    START = (START_ROOMS, 0)
    END = [(TARGET[i], ROOMS[i])
           for i in range(len(ROOMS))]
    END_ROOMS = tuple(sorted(END))
    END = (END_ROOMS, 0)

    TYPES = 'ABCD'
    MOVE_COSTS = (1, 10, 100, 1000)

    def was_progress(old_state, pod, pos, new_state):
        if (pod, pos) not in END_ROOMS:
            return False
        base = ROOM_TO_BASE.get(pos)
        if base is None:
            # Definite progress!
            return True
        if (pod, base) not in old_state:
            # It's not progress if the lower room isn't filled!
            return False
        if (pod, base) not in new_state:
            # This is regressing!
            return False

##        print(old_state)
##        print(pod, pos)
##        print(new_state)
##        assert(False)
        
        return True

    def neighbors(key):
        key, moves_since_progress = key
        if moves_since_progress >= 5:
            # We've stalled!
            return []

        occupied = set(pos for _,pos in key)

        options = []

        for idx, (pod, c) in enumerate(key):
            move_cost = MOVE_COSTS[TYPES.index(pod)]
            for n in grid.neighbors(*c):
                if n in occupied:
                    continue
                if grid[n] == '#':
                    continue

                if n in OUTSIDE_ROOM:
                    # We have to move again!
                    for n2 in grid.neighbors(*n):
                        if n2 in occupied:
                            continue
                        if grid[n2] == '#':
                            continue

                        new_state = tuple(sorted(key[:idx] + ((pod, n2),) + key[idx+1:]))

                        new_moves_since_progress = moves_since_progress + 1
                        if was_progress(key, pod, n2, new_state):
                            new_moves_since_progress = 0
                        new_moves_since_progress = 0

                        options.append(((new_state, new_moves_since_progress), 2*move_cost))
                else:
                    new_state = tuple(sorted(key[:idx] + ((pod, n),) + key[idx+1:]))

                    new_moves_since_progress = moves_since_progress + 1
                    if was_progress(key, pod, n, new_state):
                        new_moves_since_progress = 0
                    new_moves_since_progress = 0

                    options.append(((new_state, new_moves_since_progress), move_cost))

##        print('\n'.join(map(str, key)))
##        print()
##
##        for (o, new_moves), cost in options:
##            print(cost, new_moves)
##            print('\n'.join(map(str, o)))
##            print()
##            assert(new_moves != 0)
##
##        print('-'*75)

##        assert(False)

##        print('\n'.join(map(str, options)))

        return options

    graph = lib.graph.make_lazy_graph(neighbors)

    TARGET_COLUMN = {
        'A':3,
        'B':5,
        'C':7,
        'D':9,
    }

    def heuristic(key):
        key, _ = key

        pods_in_base = set()

        est_cost = 0
        for pod, (x, y) in key:
            cost_per_tile = MOVE_COSTS[TYPES.index(pod)]
            target_col = TARGET_COLUMN[pod]
            if x == target_col:
                if y == 3:
                    pods_in_base.add(pod)
                    continue
            tiles_to_move = abs(x - target_col)
            if x != target_col:
                tiles_to_move += y
            est_cost += cost_per_tile * tiles_to_move
        for pod in 'ABCD':
            # And move them to the base if necessary
            cost_per_tile = MOVE_COSTS[TYPES.index(pod)]
            if pod not in pods_in_base:
                est_cost += cost_per_tile
        return est_cost

    answer = lib.graph.dijkstra_length(graph, START, END, heuristic)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2021, 23)
part1(INPUT)
part2(INPUT)
