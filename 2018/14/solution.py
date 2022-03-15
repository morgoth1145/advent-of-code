import lib.aoc

def part1(s):
    n = int(s)

    recipes = [3, 7]
    e0, e1 = 0, 1

    while len(recipes) < n + 10:
        combined = recipes[e0] + recipes[e1]
        if combined > 9:
            recipes.append(1)
        recipes.append(combined % 10)

        e0 = (e0 + 1 + recipes[e0]) % len(recipes)
        e1 = (e1 + 1 + recipes[e1]) % len(recipes)

    answer = ''.join(map(str, recipes[n:n+10]))

    print(f'The answer to part one is {answer}')

def part2(s):
    target = list(map(int, s))
    most_recent = [-1] * len(target)
    most_recent = most_recent[2:] + [3, 7]

    recipes = [3, 7]
    e0, e1 = 0, 1

    while True:
        combined = recipes[e0] + recipes[e1]
        if combined > 9:
            recipes.append(1)
            most_recent = most_recent[1:] + [1]
            if most_recent == target:
                break
        recipes.append(combined % 10)
        most_recent = most_recent[1:] + [recipes[-1]]
        if most_recent == target:
            break

        e0 = (e0 + 1 + recipes[e0]) % len(recipes)
        e1 = (e1 + 1 + recipes[e1]) % len(recipes)

    answer = len(recipes) - len(target)

    print(f'The answer to part two is {answer}')

INPUT = lib.aoc.get_input(2018, 14)
part1(INPUT)
part2(INPUT)
