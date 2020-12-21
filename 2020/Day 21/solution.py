import re

import helpers.input

def parse_foods(s):
    foods = []
    all_ingredients = set()
    all_allergens = set()
    for line in s.splitlines():
        m = re.fullmatch('([a-zA-Z ]+) \(contains ([a-zA-Z ,]+)\)', line)
        ingredients = set(m.group(1).split())
        allergens = set(m.group(2).split(', '))
        all_ingredients |= ingredients
        all_allergens |= allergens
        foods.append((ingredients, allergens))
    return foods, all_ingredients, all_allergens

def find_allergen_containing_ingredients(foods, all_ingredients, all_allergens):
    allergen_to_ingredients = {allergen:set(all_ingredients)
                               for allergen in all_allergens}

    for ingredients, allergens in foods:
        for allergen in allergens:
            allergen_to_ingredients[allergen] &= ingredients

    isolated_ingredients = set()
    while len(isolated_ingredients) < len(all_allergens):
        for ingredients in allergen_to_ingredients.values():
            if len(ingredients) == 1:
                isolated_ingredients |= ingredients
        for ingredients in allergen_to_ingredients.values():
            if len(ingredients) > 1:
                ingredients -= isolated_ingredients

    return {allergen:list(ingredients)[0]
            for allergen,ingredients in allergen_to_ingredients.items()}

def part1(s):
    foods, all_ingredients, all_allergens = parse_foods(s)
    allergen_to_ingredient = find_allergen_containing_ingredients(foods,
                                                                  all_ingredients,
                                                                  all_allergens)

    bad_ingredients = set(allergen_to_ingredient.values())

    answer = 0
    for ingredients, allergens in foods:
        answer += len(ingredients - bad_ingredients)
    print(f'The answer to part one is {answer}')

def part2(s):
    allergen_to_ingredient = find_allergen_containing_ingredients(*parse_foods(s))

    answer = ','.join(ingredient
                      for _,ingredient
                      in sorted(allergen_to_ingredient.items()))

    print(f'The answer to part two is {answer}')

INPUT = helpers.input.get_input(2020, 21)

part1(INPUT)
part2(INPUT)
