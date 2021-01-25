"""
--- Day 21: Allergen Assessment ---

You reach the train's last stop and the closest you can get to your vacation island without getting wet. There aren't
even any boats here, but nothing can stop you now: you build a raft. You just need a few days' worth of food for your
journey.
You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens are listed in
 a language you do understand. You should be able to use this information to determine which ingredient contains which
 allergen and work out which foods are safe to take with you on your trip.
You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's
ingredients list followed by some or all of the allergens the food contains.
Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen. Allergens aren't always
 marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list), the ingredient that contains
 each listed allergen will be somewhere in the corresponding ingredients list. However, even if an allergen isn't
 listed, the ingredient that contains that allergen could still be present: maybe they forgot to label it, or maybe it
 was labeled in a language you don't know.
For example, consider the following list of foods:

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)

The first food in the list has four ingredients (written in a language you don't understand): mxmxvkd, kfcds, sqjhc, and
 nhms. While the food might contain other allergens, a few allergens the food definitely contains are listed afterward:
 dairy and fish.
The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list.
In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen. Counting the number of
 times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which
  appears twice.
Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those
ingredients appear?


"""
import os
import re
import time
from collections import defaultdict
from typing import NamedTuple, Set, Iterable, Dict, Tuple, List

DEBUG = False


FOOD_REGEX = re.compile(r"(.*?) \(contains (.*)\)")


class Food(NamedTuple):
    ingredients: Set[str]
    allergens: Set[str]


def _parse(lines: Iterable[str]) -> Iterable[Food]:
    return map(_parse_food, lines)


def _parse_food(line: str) -> Food:
    matcher = FOOD_REGEX.search(line.strip())
    if not matcher or len(matcher.groups()) != 2:
        raise ValueError(f"Unable to parse food: {line}")

    return Food(
        ingredients=set(matcher.group(1).split()),
        allergens=set(matcher.group(2).split(", "))
    )


def solve_part1(foods: List[Food]) -> int:
    managing_to_reduce = True
    while managing_to_reduce:
        managing_to_reduce = False
        ingredients_by_allergen: Dict[str, Set[str]] = {}
        for food in foods:
            for allergen in food.allergens:
                ingredients_by_allergen[allergen] = food.ingredients \
                    if allergen not in ingredients_by_allergen \
                    else ingredients_by_allergen[allergen] & food.ingredients

        matches: List[Tuple[str, str]] = []
        for allergen, ingredients in ingredients_by_allergen.items():
            if len(ingredients) == 1:
                matches.append((allergen, ingredients.pop()))

        if matches:
            foods = list(map(
                lambda f: _remove_known_allergens(f, matches),
                foods
            ))
            managing_to_reduce = True

    safe_ingredients = defaultdict(int)
    for food in foods:
        if not food.allergens:
            for ingredient in food.ingredients:
                safe_ingredients[ingredient] += 1

    return sum(safe_ingredients.values())


def _remove_known_allergens(food: Food, known_allergens: List[Tuple[str, str]]) -> Food:
    allergens = set(food.allergens)
    ingredients = set(food.ingredients)
    for allergen, ingredient in known_allergens:
        if ingredient in ingredients:
            ingredients.remove(ingredient)
            if allergen in allergens:
                allergens.remove(allergen)

    return Food(ingredients, allergens)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _foods = list(_parse(file.readlines()))

        start = time.time()
        solution_part1 = solve_part1(_foods)
        end = time.time()
        print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        assert solution_part1 == 2230
