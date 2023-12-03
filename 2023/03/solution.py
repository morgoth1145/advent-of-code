import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    symbol_positions = set()

    for coord, c in grid.items():
        if c == '.' or c.isdigit():
            continue
        symbol_positions.add(coord)

    answer = 0

    for y in range(grid.height):
        num = None
        num_start_x = None
        def handle_num(end_x):
            nonlocal num, num_start_x
            nonlocal answer

            num = int(num)

            border = set()
            for check_x in range(num_start_x-1, x+1):
                border.add((check_x, y-1))
                border.add((check_x, y+1))
            border.add((num_start_x-1, y))
            border.add((x, y))

            if len(border & symbol_positions) > 0:
                # Borders a symbol!
                answer += num

            num = None
            num_start_x = None

        for x in range(grid.width):
            c = grid[x,y]
            if c.isdigit():
                if num is None:
                    num = c
                    num_start_x = x
                else:
                    num += c
            else:
                if num is not None:
                    # x is one past the number's end
                    handle_num(x)

        if num is not None:
            handle_num(grid.width)

    lib.aoc.give_answer(2023, 3, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2023, 3)

part1(INPUT)
part2(INPUT)
