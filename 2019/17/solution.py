import lib.aoc
import lib.grid

intcode = __import__('2019.intcode').intcode

def get_scaffold_grid(s):
    _, out_chan = intcode.Program(s).run()

    return lib.grid.FixedGrid.parse(''.join(map(chr, out_chan)).strip())

def part1(s):
    grid = get_scaffold_grid(s)

    answer = sum(x*y
                 for (x, y), c in grid.items()
                 if c == '#'
                 if all(grid[n] == '#' for n in grid.neighbors(x, y))
                 if len(list(grid.neighbors(x, y))) == 4)

    print(f'The answer to part one is {answer}')

def extract_path(s):
    grid = get_scaffold_grid(s).to_dict()

    x, y = next(coord
                for coord, c in grid.items()
                if c == '^')
    dx, dy = 0, -1

    steps = []

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
            return steps # Must be done

        steps.append(turn)

        move_units = 0
        while grid.get((x+dx, y+dy)) == '#':
            move_units += 1
            x += dx
            y += dy

        steps.append(move_units)

MAX_SEQUENCE_LENGTH = 20
SUBPROGRAM_NAMES = 'ABC'
NUM_SUBPROGRAMS = len(SUBPROGRAM_NAMES)

def compress_path(remaining_steps, main_sequence=tuple(), subprograms=tuple()):
    if len(','.join(main_sequence)) > MAX_SEQUENCE_LENGTH:
        return None

    if len(remaining_steps) == 0:
        main_sequence = ','.join(main_sequence)

        subprograms = [','.join(map(str, subprogram))
                       for subprogram in subprograms]
        while len(subprograms) < NUM_SUBPROGRAMS:
            subprograms.append('')

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
            compressed = compress_path(remaining_steps[subprogram_len:],
                                       main_sequence + (SUBPROGRAM_NAMES[subprogram_idx],),
                                       subprograms)
            if compressed is not None:
                return compressed
        elif (isinstance(last_step, int) and
              isinstance(remaining_steps[subprogram_len-1], int) and
              last_step < remaining_steps[subprogram_len-1]):
            new_remaining = list(remaining_steps[subprogram_len-1:])
            new_remaining[0] -= last_step
            compressed = compress_path(new_remaining,
                                       main_sequence + (SUBPROGRAM_NAMES[subprogram_idx],),
                                       subprograms)
            if compressed is not None:
                return compressed

    if len(subprograms) == NUM_SUBPROGRAMS:
        return None

    # Try to find a new subprogram
    cand_subprogram = list(remaining_steps)

    def trim_cand_subprogram():
        if isinstance(cand_subprogram[-1], int):
            cand_subprogram[-1] -= 1
            if cand_subprogram[-1] == 0:
                cand_subprogram.pop(-1)
        else:
            cand_subprogram.pop(-1)

    while len(','.join(map(str, cand_subprogram))) > MAX_SEQUENCE_LENGTH:
        trim_cand_subprogram()

    while cand_subprogram:
        compressed = compress_path(remaining_steps,
                                   main_sequence,
                                   subprograms + (tuple(cand_subprogram),))
        if compressed is not None:
            return compressed

        # The subprogram didn't work, trim it
        trim_cand_subprogram()

def part2(s):
    main, subprograms = compress_path(extract_path(s))

    bot_commands = '\n'.join([main] + subprograms + ['n']) + '\n'

    p = intcode.Program(s)
    p.memory[0] = 2 # Wake up robot
    in_chan, out_chan = p.run()

    for c in map(ord, bot_commands):
        in_chan.send(c)

    answer = list(out_chan)[-1]

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2019, 17)
part1(INPUT)
part2(INPUT)
