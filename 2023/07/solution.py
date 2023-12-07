import collections

import lib.aoc

def classify(hand):
    stats = sorted(collections.Counter(hand).values())
    if stats == [5]:            return 6 # Five of a kind
    if stats == [1, 4]:         return 5 # Four of a kind
    if stats == [2, 3]:         return 4 # Full house
    if stats == [1, 1, 3]:      return 3 # Three of a kind
    if stats == [1, 2, 2]:      return 2 # Two pair
    if stats == [1, 1, 1, 2]:   return 1 # One pair
    return 0 # High card

def solve(s, card_rank_order, hand_fixer=None):
    hands = []

    for line in s.splitlines():
        hand, bid = line.split()
        hand_to_classify = hand if hand_fixer is None else hand_fixer(hand)

        t = classify(hand_to_classify)
        ranks = tuple(map(card_rank_order.index, hand))
        hands.append((t, ranks, int(bid)))

    return sum(rank * bid
               for rank, (_, _, bid)
               in enumerate(sorted(hands), start=1))

def part1(s):
    answer = solve(s, '23456789TJQKA')

    lib.aoc.give_answer(2023, 7, 1, answer)

PART2_CARD_RANK_ORDER = 'J23456789TQKA'

def wild_substituter(hand):
    counts = collections.Counter(hand)
    jokers = counts.pop('J', 0)
    if jokers == 5:
        return 'AAAAA'

    # Replace jokers with the strongest of the most common cards
    # This will be the strongest hand possible
    target_count = max(counts.values())
    target = max((c for c, count in counts.items()
                  if count == target_count),
                 key=PART2_CARD_RANK_ORDER.index)
    return hand.replace('J', target)

def part2(s):
    answer = solve(s, PART2_CARD_RANK_ORDER, wild_substituter)

    lib.aoc.give_answer(2023, 7, 2, answer)

INPUT = lib.aoc.get_input(2023, 7)
part1(INPUT)
part2(INPUT)
