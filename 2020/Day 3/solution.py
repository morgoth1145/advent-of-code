import helpers.input

def count_tree_hits(s, right, down=1):
    answer = 0
    x = 0
    for line in s.splitlines()[::down]:
        if line[x] == '#':
            answer += 1
        x = (x + right) % len(line)
    return answer

def part1(s):
    answer = count_tree_hits(s, 3)
    print(f'The answer to part one is {answer}')

def part2(s):
    answer = 1
    for right in (1, 3, 5, 7):
        answer *= count_tree_hits(s, right)
    answer *= count_tree_hits(s, 1, 2)
    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 3)
part1(INPUT)
part2(INPUT)
