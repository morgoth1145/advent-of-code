import heapq

import lib.aoc

class Block:
    def __init__(self, file_id, pos, length):
        self.file_id = file_id
        self.pos = pos
        self.length = length

    @property
    def heap_num(self):
        # Treat free blocks longer than 9 as length 9 for the sake of heaps
        # This works since files are at most length 9
        return min(self.length, 9)

    def __lt__(self, other):
        return self.pos < other.pos

def solve(s, split_files_into_single_blocks=False):
    files = []
    free_heaps = [[] for _ in range(10)]

    is_file = True
    next_file_id = 0
    pos = 0
    last_free_b = None

    for n in map(int, s):
        file_id = next_file_id if is_file else None
        block = Block(file_id, pos, n)
        if is_file:
            next_file_id += 1
            if n > 0:
                if split_files_into_single_blocks:
                    for off in range(n):
                        files.append((Block(file_id, pos+off, 1)))
                else:
                    files.append(block)
                last_free_b = None # Wipe the last free block to prevent merges!
        else:
            if n > 0:
                if last_free_b is not None:
                    free_heaps[last_free_b.heap_num].pop()
                    last_free_b.length += n
                    block = last_free_b
                free_heaps[block.heap_num].append(block)
                last_free_b = block
        pos += n
        is_file = not is_file

    for h in free_heaps:
        heapq.heapify(h)

    def find_free_block(target_length):
        best_length, best_b = None, None
        for length in range(target_length, 10):
            if len(free_heaps[length]) == 0:
                continue
            free_b = free_heaps[length][0]
            if best_b is None or free_b < best_b:
                best_length = length
                best_b = free_b
        if best_length is None:
            return None
        return heapq.heappop(free_heaps[best_length])

    for f in files[::-1]:
        free_b = find_free_block(f.length)
        if free_b is None or free_b.pos > f.pos:
            # Don't bother replacing free_b if it's not None, if it's past f.pos
            # then it won't be useful for any future files either
            continue

        f.pos = free_b.pos

        free_b.pos += f.length
        free_b.length -= f.length
        if free_b.length > 0:
            heapq.heappush(free_heaps[free_b.heap_num], free_b)

    files.sort()

    answer = 0
    for b in files:
        for i in range(b.length):
            answer += (b.pos+i) * b.file_id

    return answer

def part1(s):
    answer = solve(s, split_files_into_single_blocks=True)

    lib.aoc.give_answer(2024, 9, 1, answer)

def part2(s):
    answer = solve(s)

    lib.aoc.give_answer(2024, 9, 2, answer)

INPUT = lib.aoc.get_input(2024, 9)
part1(INPUT)
part2(INPUT)
