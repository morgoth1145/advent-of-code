import lib.aoc

def part1(s):
    nums = list(map(int, s))

    blocks = []
    free_spots = []

    is_file = True
    file_id = 0

    for n in nums:
        if is_file:
            for _ in range(n):
                blocks.append(file_id)
            file_id += 1
        else:
            for _ in range(n):
                idx = len(blocks)
                free_spots.append(idx)
                blocks.append(None)
        is_file = not is_file

    for pos in free_spots:
        if pos > len(blocks):
            break
        val = blocks.pop()
        blocks[pos] = val
        while blocks[-1] == None:
            blocks.pop()

    answer = 0

    for pos, v in enumerate(blocks):
        answer += pos * v

    lib.aoc.give_answer(2024, 9, 1, answer)

def part2(s):
    pass

INPUT = lib.aoc.get_input(2024, 9)
part1(INPUT)
part2(INPUT)
