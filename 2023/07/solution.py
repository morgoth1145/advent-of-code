import collections

import lib.aoc

HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OF_A_KIND = 3
FULL_HOUSE = 4
FOUR_OF_A_KIND = 5
FIVE_OF_A_KIND = 6

class Hand:
    def __init__(self, s):
        self.cards = s
        # Higher is better
        self.card_power = list(map('23456789TJQKA'.index, s))
        self.counted = collections.Counter(sorted(self.card_power))
        def stat_key(p):
            power, count = p
            return count, power
        self.stats = sorted(map(stat_key, self.counted.most_common()),
                            reverse=True)

    def classify(self):
        if self.stats[0][0] == 5:
            return FIVE_OF_A_KIND
        if self.stats[0][0] == 4:
            return FOUR_OF_A_KIND
        if self.stats[0][0] == 3:
            if self.stats[1][0] == 2:
                return FULL_HOUSE
            return THREE_OF_A_KIND
        if self.stats[0][0] == 2:
            if self.stats[1][0] == 2:
                return TWO_PAIR
            return ONE_PAIR
        return HIGH_CARD

    def __lt__(self, other):
        assert(isinstance(other, Hand))
        sc = self.classify()
        oc = other.classify()
        if sc < oc:
            return True
        if oc < sc:
            return False
        # This is weird
        return self.card_power < other.card_power

def parse_input(s):
    for line in s.splitlines():
        a, b = line.split()
        yield Hand(a), int(b)

def part1(s):
    data = sorted(parse_input(s))

    answer = sum(rank * bid
                 for rank, (hand, bid)
                 in enumerate(data, start=1))

    lib.aoc.give_answer(2023, 7, 1, answer)

class Hand2:
    def __init__(self, s):
        self.cards = s
        # Higher is better
        ORDER = 'J23456789TQKA'
        self.card_power = list(map(ORDER.index, s))
        jokers = s.count('J')
        if jokers == 5:
            best = 'A'
        else:
            # Replace jokers with the most common, most powerful card
            first = list(map(ORDER.index, s.replace('J', '')))
            first = collections.Counter(sorted(first))
            first = first.most_common()[0]
            best = first[0]
            best = ORDER[best]
        count_power = s.replace('J', best)
        self.counted = collections.Counter(sorted(count_power))
        def stat_key(p):
            power, count = p
            return count, power
        self.stats = sorted(map(stat_key, self.counted.most_common()),
                            reverse=True)

    def classify(self):
        if self.stats[0][0] == 5:
            return FIVE_OF_A_KIND
        if self.stats[0][0] == 4:
            return FOUR_OF_A_KIND
        if self.stats[0][0] == 3:
            if self.stats[1][0] == 2:
                return FULL_HOUSE
            return THREE_OF_A_KIND
        if self.stats[0][0] == 2:
            if self.stats[1][0] == 2:
                return TWO_PAIR
            return ONE_PAIR
        return HIGH_CARD

    def __lt__(self, other):
        assert(isinstance(other, Hand2))
        sc = self.classify()
        oc = other.classify()
        if sc < oc:
            return True
        if oc < sc:
            return False
        # This is weird
        return self.card_power < other.card_power

def parse_input2(s):
    for line in s.splitlines():
        a, b = line.split()
        yield Hand2(a), int(b)

def part2(s):
    data = sorted(parse_input2(s))

    answer = sum(rank * bid
                 for rank, (hand, bid)
                 in enumerate(data, start=1))

    lib.aoc.give_answer(2023, 7, 2, answer)

INPUT = lib.aoc.get_input(2023, 7)
part1(INPUT)
part2(INPUT)
