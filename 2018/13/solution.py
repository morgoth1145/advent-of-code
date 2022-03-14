import lib.aoc
import lib.grid

def part1(s):
    grid = lib.grid.FixedGrid.parse(s)

    carts = []

    for coord, c in grid.items():
        if c in ' -/\\|+':
            continue

        if c == '<':
            carts.append((coord, -1, 0))
            grid[coord] = '-'
        elif c == '>':
            carts.append((coord, 1, 0))
            grid[coord] = '-'
        elif c == '^':
            carts.append((coord, 0, -1))
            grid[coord] = '|'
        elif c == 'v':
            carts.append((coord, 0, 1))
            grid[coord] = '|'
        else:
            assert(False)

    intersection_counts = [0] * len(carts)

    while True:
        seen = set()
        crash = None

        for idx, ((x, y), dx, dy) in enumerate(carts):
            x += dx
            y += dy

            coord = x, y

            if coord in seen:
                crash = coord
                break

            seen.add(coord)

            if grid[coord] == '+':
                # Intersection
                choice = intersection_counts[idx] % 3

                if choice == 0:
                    # Turn left
                    dx, dy = dy, -dx
                elif choice == 1:
                    # Straight
                    pass
                elif choice == 2:
                    # Turn right
                    dx, dy = -dy, dx
                else:
                    assert(False)

                intersection_counts[idx] += 1
            elif grid[coord] == '/':
                # Turn right if moving vertically, turn left if moving horizontally
                dx, dy = -dy, -dx
            elif grid[coord] == '\\':
                # Turn left if moving vertically, turn right if moving horizontally
                dx, dy = dy, dx

            carts[idx] = coord, dx, dy

        if crash is not None:
            x, y = crash
            answer = f'{x},{y}'
            break

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2018, 13)
part1(INPUT)
part2(INPUT)
