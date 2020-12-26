import lib.aoc

def play_cups(seed, cup_count, turns):
    assert(sorted(seed) == list(range(1, max(seed)+1)))

    cups = [-1] + list(range(2, cup_count+1)) + [1]
    for cup, next_cup in zip(seed, seed[1:]):
        cups[cup] = next_cup
    if len(seed) < cup_count:
        cups[seed[-1]] = max(seed)+1
        cups[-1] = seed[0]
    else:
        cups[seed[-1]] = seed[0]

    min_cup = min(seed)
    current = seed[0]
    for _ in range(turns):
        p1 = cups[current]
        p2 = cups[p1]
        p3 = cups[p2]
        cups[current] = cups[p3]
        dest = current-1
        while True:
            if dest < min_cup:
                dest = cup_count
            if dest not in [p1, p2, p3]:
                break
            dest -= 1
        cups[p3] = cups[dest]
        cups[dest] = p1
        current = cups[current]
    return cups

def part1(s):
    seed = list(map(int, s))
    cups = play_cups(seed, len(seed), 100)
    order = []
    current = cups[1]
    while current != 1:
        order.append(current)
        current = cups[current]
    answer = ''.join(map(str, order))
    print(f'The answer to part one is {answer}')

def part2(s):
    cups = play_cups(list(map(int, s)), 1000000, 10000000)
    a = cups[1]
    b = cups[a]
    answer = a*b
    print(f'The answer to part one is {answer}')

INPUT = lib.aoc.get_input(2020, 23)

part1(INPUT)
part2(INPUT)
