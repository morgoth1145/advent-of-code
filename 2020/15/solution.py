import helpers.input

def get_nth_number_in_game(seed, desired_turn):
    spoken_on = {n:turn
                 for turn, n
                 in enumerate(map(int,
                                  seed.split(',')))}
    n = 0 # The seed numbers are all unique
    for turn in range(len(spoken_on), desired_turn-1):
        # Get the number of turns since the number was spoken (or 0 if it's new)
        n_next = turn - spoken_on.get(n, turn)
        spoken_on[n] = turn
        n = n_next
    return n

def part1(s):
    answer = get_nth_number_in_game(s, 2020)
    print(f'The answer to part one is {answer}')

def part2(s):
    answer = get_nth_number_in_game(s, 30000000)
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 15)

part1(INPUT)
part2(INPUT)
