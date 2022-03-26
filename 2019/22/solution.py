import lib.aoc

def parse_steps(s):
    for line in s.splitlines():
        parts = line.split()
        if parts[0] == 'cut':
            yield 'cut', int(parts[1])
            continue

        assert(parts[0] == 'deal')
        if parts[1] == 'with':
            assert(parts[2] == 'increment')
            yield 'increment', int(parts[3])
            continue

        assert(parts[1] == 'into')
        assert(parts[2] == 'new')
        assert(parts[3] == 'stack')
        yield 'reverse', 0

def shuffle(cards, steps):
    for inst, count in steps:
        if inst == 'reverse':
            cards = cards[::-1]
        elif inst == 'cut':
            cards = cards[count:] + cards[:count]
        else:
            assert(inst == 'increment')
            new_cards = [None] * len(cards)
            pos = 0
            for idx, c in enumerate(cards):
                new_cards[pos] = c
                pos = (pos + count) % len(cards)
            cards = new_cards
            assert(None not in cards)
    return cards

def part1(s):
    cards = shuffle(list(range(10007)), parse_steps(s))

    answer = cards.index(2019)

    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = lib.aoc.get_input(2019, 22)
part1(INPUT)
part2(INPUT)
