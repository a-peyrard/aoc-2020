"""
--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab
some food: all flights are currently delayed due to issues in luggage processing.
Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents;
bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible
 for these regulations considered how long they would take to enforce!
For example, consider the following rules:
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every
 vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.
You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be
 valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
In the above rules, the following options would be available to you:
    A bright white bag, which can hold your shiny gold bag directly.
    A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
    A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny
    gold bag.
    A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny
    gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.
How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you
 get all of it.)
"""
import os
import re
from collections import defaultdict
from typing import List, NamedTuple, Iterable, Dict, DefaultDict, Optional


class Bag(NamedTuple):
    contain: List[str]
    is_contained_by: List[str]


DEFINITION_REGEX = re.compile(r"^(.*?) bags contain (.*)\.$")
CONTAIN_REGEX = re.compile(r"^\d+ (.*?) bags?$")


def count_bags_containing(bags: Dict[str, Bag], bag_name: str) -> int:
    def pop(li: List[str]) -> Optional[str]:
        try:
            return li.pop()
        except IndexError:
            return None

    containers = set()
    bags_to_analyze = list(bags[bag_name].is_contained_by)
    to_analyze = pop(bags_to_analyze)
    while to_analyze:
        if to_analyze not in containers:
            containers.add(to_analyze)
            bags_to_analyze.extend(bags[to_analyze].is_contained_by)

        to_analyze = pop(bags_to_analyze)

    return len(containers)


def _parse(definitions: Iterable[str]) -> Dict[str, Bag]:
    bags = defaultdict(lambda: Bag(contain=[], is_contained_by=[]))
    for definition in definitions:
        _parse_definition(definition.rstrip(), bags)

    return bags


def _parse_definition(definition: str, bags: DefaultDict[str, Bag]) -> None:
    matcher = DEFINITION_REGEX.search(definition)
    if not matcher or len(matcher.groups()) != 2:
        raise ValueError(f"Unable to parse definition {definition}")

    bag_name = matcher.group(1)
    contain = _extract_contain(matcher.group(2))
    bags[bag_name].contain.extend(contain)
    for bag in contain:
        bags[bag].is_contained_by.append(bag_name)


def _extract_contain(contain: str) -> List[str]:
    def extract_bag_name(raw_bag: str) -> Optional[str]:
        if raw_bag == "no other bags":
            return None

        matcher = CONTAIN_REGEX.search(raw_bag)
        if not matcher or len(matcher.groups()) != 1:
            raise ValueError(f"Unable to get bag name from {raw_bag}")

        return matcher.group(1)

    return list(filter(None, map(extract_bag_name, contain.split(", "))))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        raw_definitions = list(file.readlines())

        solution_part1 = count_bags_containing(
            bags=_parse(raw_definitions),
            bag_name="shiny gold"
        )
        print(f"solution (part1): {solution_part1}")
