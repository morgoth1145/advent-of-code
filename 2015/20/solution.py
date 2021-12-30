import heapq

import lib.aoc

def gen_houses():
    queue = [(1, 1)]

    current = 1
    total = 0

    while True:
        house_n, elf_n = heapq.heappop(queue)
        if house_n > current:
            yield current, total
            current = house_n
            total = 0
            heapq.heappush(queue, (house_n, house_n))

        total += 10 * elf_n
        heapq.heappush(queue, (house_n + elf_n, elf_n))

def part1(s):
    target = int(s)

    for house_n, presents in gen_houses():
        if presents >= target:
            answer = house_n
            break

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2015, 20)
part1(INPUT)
part2(INPUT)
