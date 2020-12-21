import re

import helpers.input

def parse_foods(s):
    foods = []
    for line in s.splitlines():
        m = re.fullmatch('([a-zA-Z ]+) \(contains ([a-zA-Z ,]+)\)', line)
        ingredients = set(m.group(1).split())
        allergens = set(m.group(2).split(', '))
        foods.append((ingredients, allergens))
    return foods

def part1(s):
    foods = parse_foods(s)

    all_ingredients = set()
    all_allergens = set()

    for ingredients, allergens in foods:
        all_ingredients |= ingredients
        all_allergens |= allergens

    possible_allergens = set()

    for allergen in all_allergens:
        possibilities = set(all_ingredients)
        for ingredients, allergens in foods:
            if allergen in allergens:
                possibilities &= ingredients
        possible_allergens |= possibilities

    safe_ingredients = all_ingredients - possible_allergens

    answer = 0
    for ingredients, allergens in foods:
        answer += len(ingredients & safe_ingredients)
    print(f'The answer to part one is {answer}')

def part2(s):
    pass

INPUT = helpers.input.get_input(2020, 21)

part1(INPUT)
part2(INPUT)
