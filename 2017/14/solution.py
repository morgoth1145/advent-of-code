import lib.aoc

def knot_hash(s):
    nums = list(range(256))
    lengths = list(map(ord, s)) + [17, 31, 73, 47, 23]

    pos, skip = 0, 0

    for _ in range(64):
        for l in lengths:
            if pos+l < 256:
                # Simple reverse
                nums[pos:pos+l] = nums[pos:pos+l][::-1]
            else:
                # Complex reverse (loop around)
                to_rev = nums[pos:] + nums[:(pos+l) & 0xFF]
                to_rev = to_rev[::-1]
                nums[pos:] = to_rev[:256-pos]
                nums[:(pos+l) & 0xFF] = to_rev[256-pos:]

            pos = (pos + l + skip) & 0xFF
            skip = (skip+1) & 0xFF

    res = 0
    for i in range(0, 256, 16):
        val = 0
        for v in nums[i:i+16]:
            val = val ^ v
        res = (res << 8) + val

    return res

def part1(s):
    rows = [knot_hash(f'{s}-{row_n}') for row_n in range(128)]

    answer = 0
    for row in rows:
        answer += bin(row).count('1')

    lib.aoc.give_answer(2017, 14, 1, answer)

def part2(s):
    rows = [knot_hash(f'{s}-{row_n}') for row_n in range(128)]

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
            for n in [(x-1, y),
                      (x+1, y),
                      (x, y-1),
                      (x, y+1)]:
                if n in on_positions:
                    on_positions.remove(n)
                    to_process.append(n)

    lib.aoc.give_answer(2017, 14, 2, answer)

INPUT = lib.aoc.get_input(2017, 14)
part1(INPUT)
part2(INPUT)
