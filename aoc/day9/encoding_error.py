"""
--- Day 9: Encoding Error ---
With your neighbor happily enjoying their video game, you turn your attention to an open data port on the little screen
 in the seat in front of you.
Though the port is non-standard, you manage to connect it to your computer through the clever use of several paperclips.
 Upon connection, the port outputs a series of numbers (your puzzle input).
The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, conveniently for you, is an
old cypher with an important weakness.
XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two
 of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one
  such pair.
For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be valid, the next number
 must be the sum of two of those numbers:
    26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
    49 would be a valid next number, as it is the sum of 24 and 25.
    100 would not be valid; no two of the previous 25 numbers sum to 100.
    50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be
    different.
Suppose the 26th number is 45, and the first number (no longer an option, as it is more than 25 numbers ago) was 20.
Now, for the next number to be valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that add up to it:
    26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
    65 would not be valid, as no two of the available numbers sum to it.
    64 and 66 would both be valid, as they are the result of 19+45 and 21+45 respectively.
Here is a larger example which only considers the previous 5 numbers (and has a preamble of length 5):
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; the only
 number that does not follow this rule is 127.
The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble)
 which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?

-- Part Two ---
The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.
Again consider the above example:
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
In this list, adding up all of the numbers from 15 through 40 produces the invalid number from step 1, 127. (Of course,
the contiguous set of numbers in your actual list might be much longer.)
To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example,
 these are 15 and 47, producing 62.
What is the encryption weakness in your XMAS-encrypted list of numbers?
"""
import os
from collections import deque
from typing import Iterable, List, Deque


class Preamble:
    def __init__(self, initial: Iterable[int]):
        self._values = set(initial)

    def update(self, add: int, remove: int):
        self._values.remove(remove)
        self._values.add(add)

    def can_sum(self, target: int):
        for val in self._values:
            match = target - val
            if match in self._values:
                return True

        return False


def analyze_numbers(numbers: List[int], preamble_size: int = 25) -> int:
    preamble = Preamble(numbers[:preamble_size])
    for number_idx in range(preamble_size, len(numbers)):
        number = numbers[number_idx]
        if not preamble.can_sum(number):
            return number

        preamble.update(
            add=number,
            remove=numbers[number_idx - preamble_size]
        )

    raise ValueError("all numbers are satisfying the condition...")


def find_contiguous_set(numbers: List[int], target: int) -> List[int]:
    start_idx = 0
    end_idx = 0
    buf: Deque[int] = deque([numbers[0]])
    buf_sum = numbers[0]

    len_numbers = len(numbers)
    while buf_sum != target:
        if buf_sum < target:
            if end_idx + 1 >= len_numbers:
                raise ValueError("no contiguous set")
            # try to expand the buffer
            end_idx += 1
            new_val = numbers[end_idx]
            buf.append(new_val)
            buf_sum += new_val
        else:
            # buf is too big, let's try to shrink it
            if start_idx == end_idx:
                if end_idx + 1 >= len_numbers:
                    raise ValueError("no contiguous set")
                # we can not shrink the buffer anymore, create a new one
                end_idx += 1
                new_val = numbers[end_idx]
                buf = deque([new_val])
                buf_sum = new_val
            else:
                old_val = numbers[start_idx]
                start_idx += 1
                buf.popleft()
                buf_sum -= old_val

    return list(buf)


def generate_solution_part2(contiguous_set: List[int]):
    sorted_set = list(sorted(contiguous_set))
    return sorted_set[0] + sorted_set[-1]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        numbers_from_file = list(map(int, file.readlines()))

        solution_part1 = analyze_numbers(numbers_from_file)
        print(f"solution (part1): {solution_part1}")

        solution_part2 = generate_solution_part2(
            contiguous_set=find_contiguous_set(numbers_from_file, solution_part1)
        )
        print(f"solution (part2): {solution_part2}")
