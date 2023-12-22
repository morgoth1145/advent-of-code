import lib.aoc

def parse_input(s):
    for idx, line in enumerate(s.splitlines(), start=1):
        a, b = line.split('~')
        a = tuple(map(int, a.split(',')))
        b = tuple(map(int, b.split(',')))

        x0, y0, z0 = a
        x1, y1, z1 = b

        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        if z0 > z1:
            z0, z1 = z1, z0

        assert(x0 <= x1)
        assert(y0 <= y1)
        assert(z0 <= z1)

        yield (x0, y0, z0), (x1, y1, z1), idx

def part1(s):
    data = sorted(parse_input(s), key=lambda brick: brick[0][2])

    bricks = []

    for (x0, y0, z0), (x1, y1, z1), _ in data:
        b = set()
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                # Only the bottom and top row are needed
                for z in set([z0, z1]):
                    b.add((x,y,z))

        bricks.append(b)

    settled_positions = set()
    unsettled_positions = set()

    test = 0

    for b in bricks:
        unsettled_positions |= b
        test += len(b)

    assert(test == len(unsettled_positions))

    def fall(b):
        assert(len(b & unsettled_positions) == 0)

        while True:
            new_b = set()
            for x,y,z in b:
                new_b.add((x,y,z-1))
            assert(len(new_b & unsettled_positions) == 0)
            if len(new_b & settled_positions) != 0:
                return b # Settled
            if min(z for x,y,z in new_b) <= 0:
                return b # Settled
            b = new_b

    for idx, b in enumerate(bricks):
        unsettled_positions -= b

        b = fall(b)
        settled_positions |= b
        bricks[idx] = b

    answer = 0

    for idx, b in enumerate(bricks):
        settled_positions -= b

        assert(len(settled_positions) == test - len(b))

        was_safe = True
        tested = []
        for i2, b2 in enumerate(bricks[idx+1:]):
            tested.append(idx+1+i2)
            settled_positions -= b2
            if fall(b2) != b2:
                was_safe = False
                settled_positions |= b2
                break
            settled_positions |= b2

        if was_safe:
            answer += 1

        settled_positions |= b

        assert(len(settled_positions) == test)

    lib.aoc.give_answer(2023, 22, 1, answer)

def part2(s):
    data = sorted(parse_input(s), key=lambda brick: brick[0][2])

    bricks = []

    for (x0, y0, z0), (x1, y1, z1), _ in data:
        b = set()
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                # Only the bottom and top row are needed
                for z in set([z0, z1]):
                    b.add((x,y,z))

        bricks.append(b)

    settled_positions = set()
    unsettled_positions = set()

    test = 0

    for b in bricks:
        unsettled_positions |= b
        test += len(b)

    assert(test == len(unsettled_positions))

    def fall(b):
        assert(len(b & unsettled_positions) == 0)

        while True:
            new_b = set()
            for x,y,z in b:
                new_b.add((x,y,z-1))
            assert(len(new_b & unsettled_positions) == 0)
            if len(new_b & settled_positions) != 0:
                return b # Settled
            if min(z for x,y,z in new_b) <= 0:
                return b # Settled
            b = new_b

    for idx, b in enumerate(bricks):
        unsettled_positions -= b

        b = fall(b)
        settled_positions |= b
        bricks[idx] = b

    answer = 0

    for idx, b in enumerate(bricks):
        old_settled = set(settled_positions)

        settled_positions -= b

        for i2, b2 in enumerate(bricks[idx+1:], start=idx+1):
            settled_positions -= b2
            new_b2 = fall(b2)
            if b2 != new_b2:
                answer += 1
            settled_positions |= new_b2

        # Restore
        settled_positions = old_settled

        assert(len(settled_positions) == test)

    lib.aoc.give_answer(2023, 22, 2, answer)

INPUT = lib.aoc.get_input(2023, 22)
part1(INPUT)
part2(INPUT)
