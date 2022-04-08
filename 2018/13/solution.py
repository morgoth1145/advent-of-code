import lib.aoc
import lib.grid

class Cart:
    def __init__(self, coord, direct):
        self.coord = coord
        self.direct = direct
        self.intersect_count = 0

    def move(self):
        x, y = self.coord
        dx, dy = self.direct
        self.coord = x+dx, y+dy

    def handle_track(self, track):
        dx, dy = self.direct

        if track == '+':
            # Intersection
            choice = self.intersect_count % 3
            self.intersect_count += 1

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
        elif track == '/':
            # Turn right if moving vertically, turn left if moving horizontally
            dx, dy = -dy, -dx
        elif track == '\\':
            # Turn left if moving vertically, turn right if moving horizontally
            dx, dy = dy, dx

        self.direct = dx, dy

    def __repr__(self):
        return f'Cart({self.coord}, {self.direct}, {self.intersect_count})'

def parse_input(s):
    grid = lib.grid.FixedGrid.parse(s)

    carts = []

    for coord, c in grid.items():
        if c == '<':
            carts.append(Cart(coord, (-1, 0)))
            grid[coord] = '-'
        elif c == '>':
            carts.append(Cart(coord, (1, 0)))
            grid[coord] = '-'
        elif c == '^':
            carts.append(Cart(coord, (0, -1)))
            grid[coord] = '|'
        elif c == 'v':
            carts.append(Cart(coord, (0, 1)))
            grid[coord] = '|'

    return grid, carts

def tick(grid, carts):
    # Move carts in a top-down, then left-right fashion
    carts = sorted(carts, key=lambda c: (c.coord[1], c.coord[0]))

    locations = {cart.coord: cart
                 for cart in carts}

    crashes = []

    for cart in carts:
        if cart.coord not in locations:
            # Something ran into us already!
            continue

        # This cart is about to move
        del locations[cart.coord]

        cart.move()
        if cart.coord in locations:
            del locations[cart.coord]
            crashes.append(cart.coord)
            continue

        cart.handle_track(grid[cart.coord])

        locations[cart.coord] = cart

    carts = list(locations.values())

    return crashes, carts

def part1(s):
    grid, carts = parse_input(s)

    while True:
        crashes, carts = tick(grid, carts)
        if crashes:
            x, y = crashes[0]
            answer = f'{x},{y}'
            break

    lib.aoc.give_answer(2018, 13, 1, answer)

def part2(s):
    grid, carts = parse_input(s)

    while len(carts) > 1:
        _, carts = tick(grid, carts)

    x, y = carts[0].coord
    answer = f'{x},{y}'

    lib.aoc.give_answer(2018, 13, 2, answer)

INPUT = lib.aoc.get_input(2018, 13)
part1(INPUT)
part2(INPUT)
