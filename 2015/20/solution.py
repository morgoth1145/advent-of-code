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

def gen_houses_2():
    queue = [(mult, 1)
             for mult in range(1, 51)]

    current = 1
    total = 0

    while True:
        if queue[0][0] > current:
            yield current, total
            current += 1
            total = 0

            # Spawn a new elf
            for mult in range(1, 51):
                heapq.heappush(queue, (current * mult, current))

        house_n, elf_n = heapq.heappop(queue)
        total += 11 * elf_n

def part2(s):
    target = int(s)

    for house_n, presents in gen_houses_2():
        if presents >= target:
            answer = house_n
            break

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2015, 20)
part1(INPUT)
part2(INPUT)
