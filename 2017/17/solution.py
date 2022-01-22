import lib.aoc

def part1(s):
    steps = int(s)
    buffer = [0]

    pos = 0

    for n in range(1, 2018):
        pos = (pos + steps) % len(buffer)
        buffer.insert(pos+1, n)
        pos += 1

    answer = buffer[(buffer.index(2017)+1) % len(buffer)]

    print(f'The answer to part one is {answer}')

def part2(s):
    steps = int(s)

    pos = 0
    length = 1

    n = 1
    to_insert = 50000000-1

    while to_insert > 0:
        # See if we can do a quick jump-ahead. We only care about insertions
        # which land on 0, so we can skip iterations which don't loop around
        skip_ahead = (length - 1 - pos) // (steps + 1)
        if skip_ahead:
            # Insert the chunks so long as they're still pending
            skip_ahead = min(skip_ahead, to_insert)

            pos += steps * skip_ahead + skip_ahead
            length += skip_ahead

            to_insert -= skip_ahead
            n += skip_ahead
            continue

        pos = (pos + steps) % length + 1
        length += 1

        # If the insert location is 1 then it's the new "after 0" value
        if pos == 1:
            answer = n

        to_insert -= 1
        n += 1

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 17)
part1(INPUT)
part2(INPUT)
