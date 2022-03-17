import lib.aoc
import lib.grid

class Unit:
    def __init__(self, ap, hp, force):
        self.ap = ap
        self.hp = hp
        self.force = force

def parse_input(s):
    grid = lib.grid.FixedGrid.parse(s)
    units = {}
    force_counts = {
        'E':0,
        'G':0
    }

    for coord, c in grid.items():
        if c in 'EG':
            units[coord] = Unit(3, 200, c)
            force_counts[c] += 1

    return grid, units, force_counts

def reading_order_neighbors(x, y):
    return [(x,y-1),
            (x-1,y),
            (x+1,y),
            (x,y+1)]

def execute_round(grid, units, force_counts):
    unit_order = sorted(units.items(), key=lambda u: (u[0][1], u[0][0]))

    assert(len(unit_order) > 0)

    for coord, u in unit_order:
        if u.hp <= 0:
            # The unit died!
            continue

        if force_counts[u.force] == sum(force_counts.values()):
            # All enemy forces are dead, end the round prematurely
            return False

        x, y = coord

        first_moves = []
        attack_targets = []
        for n in reading_order_neighbors(x, y):
            nc = grid[n]
            if nc == '#':
                continue
            if nc == '.':
                first_moves.append(n)
                continue
            if nc == u.force:
                continue
            if nc in 'EG':
                attack_targets.append(n)
                continue
            assert(False)

        if not attack_targets:
            # Not adjacent to an enemy, try to move
            if len(first_moves) == 0:
                # No move possible
                continue

            moves = [(n, n) for n in first_moves]
            seen = set(moves)

            move_targets = []
            while len(moves) > 0 and len(move_targets) == 0:
                next_moves = []

                for first_move, (x, y) in moves:
                    for n in reading_order_neighbors(x, y):
                        if (first_move, n) in seen:
                            continue
                        nc = grid[n]
                        if nc == '#' or nc == u.force:
                            continue
                        if nc == '.':
                            next_moves.append((first_move, n))
                            seen.add((first_move, n))
                            continue
                        if nc in 'EG':
                            move_targets.append((first_move, (x, y)))
                            continue
                        assert(False)

                moves = next_moves

            if len(move_targets) == 0:
                # No move possible
                continue

            # Pick the right move (reading order target, then reading order move)
            moves = sorted(move_targets,
                           key=lambda m: (m[1][1], m[1][0],
                                          m[0][1], m[0][0]))

            move, move_target = moves[0]

            # Execute the move
            del units[coord]
            units[move] = u
            grid[coord] = '.'
            grid[move] = u.force

            # Check for an attack target
            x, y = move
            for n in reading_order_neighbors(x, y):
                nc = grid[n]
                if nc in '#.':
                    continue
                if nc == u.force:
                    continue
                if nc in 'EG':
                    attack_targets.append(n)
                    continue
                assert(False)

        if attack_targets:
            # Choose target by weakest, followed by reading order
            attack_targets.sort(key=lambda at: (units[at].hp, at[1], at[0]))

            # Execute attack
            attack_coord = attack_targets[0]
            target = units[attack_coord]
            target.hp -= u.ap
            if target.hp <= 0:
                # The unit is dead
                del units[attack_coord]
                grid[attack_coord] = '.'
                force_counts[target.force] -= 1

    # Executed a full round
    return True

def part1(s):
    grid, units, force_counts = parse_input(s)

    full_rounds_run = 0
    while execute_round(grid, units, force_counts):
        full_rounds_run += 1

    remaining_hp = sum(u.hp for u in units.values())

    answer = full_rounds_run * remaining_hp

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 15)
part1(INPUT)
part2(INPUT)
