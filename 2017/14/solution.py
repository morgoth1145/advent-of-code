import lib.aoc

def knot_hash(nums, pos, skip, lengths):
    nums = list(nums)

    for l in lengths:
        # Reverse
        to_rev = []
        for i in range(l):
            to_rev.append(nums[(pos + i) % len(nums)])
        for i, v in enumerate(to_rev[::-1]):
            nums[(pos + i) % len(nums)] = v

        pos = (pos + l + skip) % len(nums)
        skip += 1

    return nums, pos, skip

def determine_row(s):
    nums = list(range(256))
    lengths = list(map(ord, s)) + [17, 31, 73, 47, 23]

    pos, skip = 0, 0

    for _ in range(64):
        nums, pos, skip = knot_hash(nums, pos, skip, lengths)

    row = 0
    for i in range(0, 256, 16):
        val = 0
        for v in nums[i:i+16]:
            val = val ^ v
        row = (row << 8) + val

    return row

def part1(s):
    rows = [determine_row(f'{s}-{row_n}') for row_n in range(128)]

    answer = 0
    for row in rows:
        answer += bin(row).count('1')

    print(f'The answer to part one is {answer}')

def part2(s):
    rows = [determine_row(f'{s}-{row_n}') for row_n in range(128)]

    on_positions = set()

    for y, row in enumerate(rows):
        for x, c in enumerate(bin(row)[2:].zfill(128)):
            if c == '1':
                on_positions.add((x, y))

    answer = 0
    while on_positions:
        answer += 1

        to_process = [list(on_positions)[0]]
        on_positions.remove(to_process[0])

        while to_process:
            x, y = to_process.pop(-1)
            for dx in (-1, 1):
                n = (x+dx, y)
                if n in on_positions:
                    on_positions.remove(n)
                    to_process.append(n)
            for dy in (-1, 1):
                n = (x, y+dy)
                if n in on_positions:
                    on_positions.remove(n)
                    to_process.append(n)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2017, 14)
part1(INPUT)
part2(INPUT)
