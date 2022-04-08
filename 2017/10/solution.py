import lib.aoc

def part1(s):
    nums = list(range(256))

    pos, skip = 0, 0

    for l in map(int, s.split(',')):
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

    answer = nums[0] * nums[1]

    lib.aoc.give_answer(2017, 10, 1, answer)

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

def part2(s):
    answer = hex(knot_hash(s))[2:].zfill(32)

    lib.aoc.give_answer(2017, 10, 2, answer)

INPUT = lib.aoc.get_input(2017, 10)
part1(INPUT)
part2(INPUT)
