"""
--- Day 5: Binary Boarding ---

You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is
yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport
control.
You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input);
perhaps you can find your seat through process of elimination.
Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like
 FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".
The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane
(numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole
list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127).
The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.
For example, consider just the first seven characters of FBFBBFFRLR:
    Start by considering the whole range, rows 0 through 127.
    F means to take the lower half, keeping rows 0 through 63.
    B means to take the upper half, keeping rows 32 through 63.
    F means to take the lower half, keeping rows 32 through 47.
    B means to take the upper half, keeping rows 40 through 47.
    B keeps rows 44 through 47.
    F keeps rows 44 through 45.
    The final F keeps the lower of the two, row 44.
The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane
(numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep
the lower half, while R means to keep the upper half.
For example, consider just the last 3 characters of FBFBBFFRLR:
    Start by considering the whole range, columns 0 through 7.
    R means to take the upper half, keeping columns 4 through 7.
    L means to take the lower half, keeping columns 4 through 5.
    The final R keeps the upper of the two, column 5.
So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.
Here are some other boarding passes:
    BFFFBBFRRR: row 70, column 7, seat ID 567.
    FFFBBBFRRR: row 14, column 7, seat ID 119.
    BBFFBBFRLL: row 102, column 4, seat ID 820.
As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?

"""
import os
from functools import reduce
from typing import NamedTuple, Tuple, List, Iterable


class Seat(NamedTuple):
    row: int
    column: int


def get_seat_from_boarding_pass(boarding_pass: str) -> Seat:
    raw_row = boarding_pass[:7]
    raw_column = boarding_pass[7:]

    return Seat(
        row=replay_binary_search((0, 127), map(lambda c: 1 if c == "B" else 0, raw_row)),
        column=replay_binary_search((0, 7), map(lambda c: 1 if c == "R" else 0, raw_column)),
    )


def calculate_seat_id(seat: Seat) -> int:
    return (seat.row * 8) + seat.column


def replay_binary_search(bounds: Tuple[int, int], steps: Iterable[int]) -> int:
    def middle(lower: int, upper: int) -> int:
        return lower + int((upper - lower) / 2)

    def reducer(acc: Tuple[int, int], cur: int) -> Tuple[int, int]:
        if cur:
            return middle(acc[0], acc[1]) + 1, acc[1]
        return acc[0], middle(acc[0], acc[1])

    return reduce(reducer, steps, bounds)[0]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        boarding_passes = list(map(str.rstrip, file.readlines()))

        solution_part1 = max(
            map(
                calculate_seat_id,
                map(
                    get_seat_from_boarding_pass,
                    boarding_passes
                )
            )
        )
        print(f"solution (part1): {solution_part1}")
