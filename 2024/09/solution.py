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
    nums = list(map(int, s))

    blocks = []
    file_starts = []

    is_file = True
    file_id = 0

    for n in nums:
        if is_file:
            file_starts.append(len(blocks))
            for _ in range(n):
                blocks.append(file_id)
            file_id += 1
        else:
            for _ in range(n):
                blocks.append(None)
        is_file = not is_file

    def find_first_gap(target_length):
        for idx, v in enumerate(blocks):
            if v is None and idx+target_length <= len(blocks):
                if all(blocks[idx+i] is None
                       for i in range(target_length)):
                    return idx
        return None

    while file_starts:
        idx = file_starts.pop()
        file_id = blocks[idx]
        end = idx
        while end+1 < len(blocks) and blocks[end+1] == file_id:
            end += 1
        length = end - idx + 1

        dest = find_first_gap(length)
        if dest is None:
            continue
        if dest < idx:
            for i in range(length):
                blocks[dest+i] = file_id
                blocks[idx+i] = None

    answer = 0

    for pos, v in enumerate(blocks):
        if v is not None:
            answer += pos * v

    lib.aoc.give_answer(2024, 9, 2, answer)

INPUT = lib.aoc.get_input(2024, 9)
part1(INPUT)
part2(INPUT)
