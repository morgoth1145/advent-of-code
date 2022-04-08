import collections
import functools
import itertools

import lib.aoc

def parse_initial_positions(s):
    return list(int(l.split()[4])
                for l in s.splitlines())

def part1(s):
    p1, p2 = parse_initial_positions(s)
    s1, s2 = 0, 0

    die = 1
    rolls = 0

    def play(player):
        nonlocal die
        nonlocal rolls
        rolls += 3
        player = (player + 3 * die + 2) % 10 + 1
        # The board is only 10 long, a 10 sided die and 100 sided die
        # are equivalent for the game
        die = (die + 3) % 10
        return player

    while True:
        p1 = play(p1)
        s1 += p1
        if s1 >= 1000:
            break
        p2 = play(p2)
        s2 += p2
        if s2 >= 1000:
            break

    answer = rolls * min(s1, s2)

    lib.aoc.give_answer(2021, 21, 1, answer)

def compute_quantum_moves_to_winning_universes(max_tile, target_score, die):
    # Precompute the moves for slightly faster runtime
    QUANTUM_MOVES = collections.Counter(sum(rolls) % max_tile
                                        for rolls
                                        in itertools.product(range(1, die+1),
                                                             repeat=3))

    # Compute the moves to win frequency for all positions
    moves_to_win = [[None] * max_tile for _ in range(target_score)]
    for cur_score in range(target_score-1, -1, -1):
        for tile in range(max_tile):
            totals = collections.Counter()
            for move, universes in QUANTUM_MOVES.items():
                new_tile = (tile + move) % max_tile
                new_score = cur_score + new_tile + 1
                if new_score >= target_score:
                    totals[1] += universes
                else:
                    next_totals = moves_to_win[new_score][new_tile]
                    for next_moves, next_universes in next_totals.items():
                        totals[next_moves+1] += universes * next_universes
            moves_to_win[cur_score][tile] = totals

    return moves_to_win[0]

def compute_winning_universe_counts(positions, position_to_moves, die):
    player_moves = [sorted(position_to_moves[p-1].items(), reverse=True)
                    for p in positions]

    wins = [0] * len(positions)
    player_universes = [1] * len(positions)
    remaining_players = len(positions)

    turn = 0
    while remaining_players:
        for idx, moves in enumerate(player_moves):
            if 0 == len(moves):
                # This player was eliminated already!
                continue
            player_universes[idx] *= die ** 3
            if moves[-1][0] == turn+1:
                _, winning_universes = moves.pop(-1)
                player_universes[idx] -= winning_universes
                for j, ou in enumerate(player_universes):
                    if idx != j:
                        winning_universes *= ou
                wins[idx] += winning_universes
                if 0 == len(moves):
                    remaining_players -= 1
        turn += 1

    return wins

def count_winning_universes(positions, max_tile, target_score, die):
    position_to_moves = compute_quantum_moves_to_winning_universes(max_tile,
                                                                   target_score,
                                                                   die)
    return compute_winning_universe_counts(positions,
                                           position_to_moves,
                                           die)

# Bonus, not used for the actual problem
def compute_all_game_outcomes(max_tile, target_score, die, players):
    position_to_moves = compute_quantum_moves_to_winning_universes(max_tile,
                                                                   target_score,
                                                                   die)
    results = {}
    for start in itertools.product(range(1, max_tile+1), repeat=players):
        results[start] = compute_winning_universe_counts(start,
                                                         position_to_moves,
                                                         die)

    return results

# Bonus, not used for the actual problem
def print_win_ratio_grid(max_tile, target_score, die):
    results = compute_all_game_outcomes(max_tile, target_score, die, 2)

    for p2 in range(1, max_tile+1):
        out = []
        for p1 in range(1, max_tile+1):
            w1, w2 = results[p1,p2]
            ratio = w1 / (w1 + w2)
            out.append(f'{ratio:0.2%}')
        print('\t'.join(out))

def part2(s):
    answer = max(count_winning_universes(parse_initial_positions(s),
                                         10,
                                         21,
                                         3))

    lib.aoc.give_answer(2021, 21, 2, answer)

INPUT = lib.aoc.get_input(2021, 21)
part1(INPUT)
part2(INPUT)
