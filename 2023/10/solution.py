import lib.aoc
import lib.grid

def find_loop(grid):
    start = next(coord
                 for coord, c in grid.items()
                 if c == 'S')

    def get_connections(x,y):
        c = grid[x,y]
        if c == '|':
            return [(x,y-1), (x,y+1)]
        elif c == '-':
            return [(x-1,y), (x+1,y)]
        elif c == 'L':
            return [(x,y-1), (x+1,y)]
        elif c == 'J':
            return [(x-1,y), (x,y-1)]
        elif c == '7':
            return [(x-1,y), (x,y+1)]
        elif c == 'F':
            return [(x,y+1), (x+1,y)]
        else:
            assert(False)

    positions = [start]
    loop = set()

    steps = 0

    while positions:
        loop.update(positions)
        next_positions = set()

        for x,y in positions:
            if grid[x,y] == 'S':
                cands = set(n
                            for n in [(x-1,y),
                                      (x,y-1),
                                      (x,y+1),
                                      (x+1,y)]
                            if (n in grid and
                                grid[n] != '.' and
                                (x,y) in get_connections(*n)))

                # Update the start tile for part 2 logic
                for t in '|-LJ7F':
                    grid[x,y] = t
                    if set(get_connections(x,y)) == cands:
                        break
            else:
                cands = get_connections(x,y)

            for n in cands:
                if n not in grid or n in loop:
                    continue
                next_positions.add(n)

        positions = list(next_positions)
        if len(positions) > 0:
            steps += 1

    return loop, steps

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    _, answer = find_loop(grid)

    lib.aoc.give_answer(2023, 10, 1, answer)

def part2(s):
    grid = lib.grid.FixedGrid.parse(s)

    loop, _ = find_loop(grid)

    # Note: FJ and L7 are functionally a single vertical pipe.
    # Don't over-count!
    VERTICAL_SECTIONS = ('FJ', 'L7', '|')
    SECTION_BEGINS = 'FL'
    SECTION_ENDS = 'J7|'

    answer = 0

    # Count enclosed tiles by tracking parity per row.
    # If an odd number of vertical tiles have been seen then any ground tiles
    # are enclosed, otherwise they are outside. This is similar to checking
    # if an arbitrary point is enclosed n an arbitrary polygon.
    for y in range(grid.height):
        is_enclosed = False
        current_section = ''
        for x in range(grid.width):
            if (x,y) in loop:
                c = grid[x,y]
                if c in SECTION_BEGINS:
                    current_section = c
                elif c in SECTION_ENDS:
                    current_section += c
                    if current_section in VERTICAL_SECTIONS:
                        is_enclosed = not is_enclosed
                    current_section = ''
            else:
                if is_enclosed:
                    answer += 1

        assert(not is_enclosed)

    lib.aoc.give_answer(2023, 10, 2, answer)

INPUT = lib.aoc.get_input(2023, 10)
part1(INPUT)
part2(INPUT)
