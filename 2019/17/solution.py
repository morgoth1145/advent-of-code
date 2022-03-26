import lib.aoc
import lib.grid

intcode = __import__('2019.intcode').intcode

def get_scaffold_grid(s):
    _, out_chan = intcode.Program(s).run()

    return lib.grid.FixedGrid.parse(''.join(map(chr, out_chan)).strip())

def part1(s):
    grid = get_scaffold_grid(s)

    answer = 0

    for (x, y), c in grid.items():
        if c != '#':
            continue

        neighbors = list(grid.neighbors(x, y))
        if len(neighbors) != 4:
            continue

        if all(grid[n] == '#' for n in neighbors):
            answer += x*y

    print(f'The answer to part one is {answer}')

def part2(s):
    grid = get_scaffold_grid(s).to_dict()

    x, y = next(coord
                for coord, c in grid.items()
                if c == '^')
    dx, dy = 0, -1

    raw_steps = []

    while True:
        turn_options = [('L', dy, -dx),
                        ('R', -dy, dx)]

        good_turn = False
        for turn, dx, dy in turn_options:
            n = (x+dx, y+dy)
            if grid.get(n) == '#':
                good_turn = True
                break

        if not good_turn:
            break # Must be done

        raw_steps.append(turn)

        move_units = 0
        while grid.get((x+dx, y+dy)) == '#':
            move_units += 1
            x += dx
            y += dy

        raw_steps.append(move_units)

    MAX_SEQUENCE_LENGTH = 20
    MAX_SUBPROGRAMS = 3

    def find_solution(remaining_steps, main_sequence, subprograms):
        if len(','.join(map(str, main_sequence))) > MAX_SEQUENCE_LENGTH:
            return None

        if len(remaining_steps) == 0:
            return main_sequence, subprograms

        for subprogram_idx, subprogram in enumerate(subprograms):
            subprogram_len = len(subprogram)
            if len(remaining_steps) < subprogram_len:
                continue

            if not all(remaining_steps[idx] == step
                       for idx, step in enumerate(subprogram[:-1])):
                # This subprogram can't match the next step
                continue

            last_step = subprogram[-1]
            if last_step == remaining_steps[subprogram_len-1]:
                solution = find_solution(remaining_steps[subprogram_len:],
                                         main_sequence + (subprogram_idx,),
                                         subprograms)
                if solution is not None:
                    return solution
            elif (isinstance(last_step, int) and
                  isinstance(remaining_steps[subprogram_len-1], int) and
                  last_step < remaining_steps[subprogram_len-1]):
                new_remaining = list(remaining_steps[subprogram_len-1:])
                new_remaining[0] -= last_step
                solution = find_solution(new_remaining,
                                         main_sequence + (subprogram_idx,),
                                         subprograms)
                if solution is not None:
                    return solution

        if len(subprograms) == MAX_SUBPROGRAMS:
            return None

        # Try to find a new subprogram
        cand_subprogram = []

        for step in remaining_steps:
            cand_subprogram.append(step)

            if len(','.join(map(str, cand_subprogram))) >= MAX_SEQUENCE_LENGTH:
                break

        while len(','.join(map(str, cand_subprogram))) > MAX_SEQUENCE_LENGTH:
            if isinstance(cand_subprogram[-1], int):
                cand_subprogram[-1] -= 1
                if cand_subprogram[-1] == 0:
                    cand_subprogram.pop(-1)
            else:
                cand_subprogram.pop(-1)

        while cand_subprogram:
            solution = find_solution(remaining_steps,
                                     main_sequence,
                                     subprograms + (tuple(cand_subprogram),))
            if solution is not None:
                return solution

            # The subprogram didn't work, trim it
            if isinstance(cand_subprogram[-1], int):
                cand_subprogram[-1] -= 1
                if cand_subprogram[-1] == 0:
                    cand_subprogram.pop(-1)
            else:
                cand_subprogram.pop(-1)

    main, subprograms = find_solution(raw_steps, tuple(), tuple())

    main = ','.join('ABC'[subprogram] for subprogram in main)

    assert(len(main) <= MAX_SEQUENCE_LENGTH)

    subprograms = [','.join(map(str, subprogram))
                   for subprogram in subprograms]

    assert(all(len(subprogram) <= MAX_SEQUENCE_LENGTH
               for subprogram in subprograms))

    p = intcode.Program(s)
    p.memory[0] = 2 # Wake up robot
    in_chan, out_chan = p.run()

    for routine in [main] + subprograms:
        for c in routine:
            in_chan.send(ord(c))
        in_chan.send(ord('\n'))

    # Turn off continuous video feed
    in_chan.send(ord('n'))
    in_chan.send(ord('\n'))

    answer = list(out_chan)[-1]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 17)
part1(INPUT)
part2(INPUT)
