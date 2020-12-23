"""
--- Day 1: Report Repair ---

After saving Christmas five years in a row, you've decided to take a vacation at a nice resort on a tropical island.
Surely, Christmas will go on without you.
The tropical island has its own currency and is entirely cash-only. The gold coins used there have a little picture of
a starfish; the locals just call them stars. None of the currency exchanges seem to have heard of them, but somehow,
you'll need to find fifty of these coins by the time you arrive so you can pay the deposit on your room.
To save your vacation, you need to get all fifty stars by December 25th.
Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second
puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!
Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input); apparently,
something isn't quite adding up.
Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.
For example, suppose your expense report contained the following:
1721
979
366
299
675
1456
In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579,
so the correct answer is 514579.
Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply
them together?

--- Part Two ---

The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from
 a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same
 criteria.
Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together
produces the answer, 241861950.
In your expense report, what is the product of the three entries that sum to 2020?

"""
import os
from typing import List, Tuple, Optional, Dict


def calculate_expense(numbers: List[int]) -> int:
    res = _two_sum(numbers, 2020)
    if not res:
        return 0

    return numbers[res[0]] * numbers[res[1]]


def calculate_expense_part2(numbers: List[int]) -> int:
    res = _three_sum(numbers, 2020)
    if not res:
        return 0

    return numbers[res[0]] * numbers[res[1]] * numbers[res[2]]


def _two_sum(numbers: List[int], sum_to_find: int) -> Optional[Tuple[int, int]]:
    """
    Find the two indexes of numbers in the initial list that have a sum equals to "sum".
    Args:
        numbers:
        sum_to_find:

    Returns: A tuple of indexes if a solution s found.
    """
    available_numbers: Dict[int, int] = {}
    for idx, current in enumerate(numbers):
        looking_for = sum_to_find - current

        looking_for_index = available_numbers.get(looking_for)
        if looking_for_index is not None:
            return looking_for_index, idx

        available_numbers[current] = idx

    return None


def _three_sum(numbers: List[int], sum_to_find: int) -> Optional[Tuple[int, int, int]]:
    """
    Find the three indexes of numbers in the initial list that have a sum equals to "sum".
    Args:
        numbers:
        sum_to_find:

    Returns: A tuple of indexes if a solution s found.
    """
    available_numbers: Dict[int, int] = {}
    for i, first in enumerate(numbers):
        for j in range(i + 1, len(numbers)):
            second = numbers[j]
            looking_for = sum_to_find - first - second
            looking_for_index = available_numbers.get(looking_for)
            if looking_for_index is not None:
                return looking_for_index, i, j

        available_numbers[first] = i

    return None


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as f:
        input_numbers = [
            int(line)
            for line in f.readlines()
            if line
        ]

        solution = calculate_expense(input_numbers)
        print(f"solution (part1): {solution}")

        solution_part2 = calculate_expense_part2(input_numbers)
        print(f"solution (part2): {solution_part2}")
