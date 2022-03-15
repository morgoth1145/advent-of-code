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
    pass

INPUT = lib.aoc.get_input(2018, 14)
part1(INPUT)
part2(INPUT)
