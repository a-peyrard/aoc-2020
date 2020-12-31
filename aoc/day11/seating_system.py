"""
--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the
 tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you
 realize you're so early, nobody else has even arrived yet!
By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can
predict the best place to sit. You make a quick map of the seat layout (your puzzle input).
The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#).
For example, the initial seat layout might look like this:
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and
always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat
(one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are
applied to every seat simultaneously:
    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.
After one round of these rules, every seat in the example layout becomes occupied:
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats become empty again:
#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:
#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##

#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##

#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no
seats to change state! Once people stop moving around, you count 37 occupied seats.
Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up
occupied?
"""
import os
from typing import List, Iterable, Callable, Optional

OCCUPIED_SEAT = "#"
EMPTY_SEAT = "L"
FLOOR = "."


def fill_seats(seats: List[List[str]]) -> int:
    counter = 0
    number_of_modifications = 0
    while counter == 0 or number_of_modifications > 0:
        seat_predicate: Callable[[str], bool]
        change_seat_state: Callable[[int], Optional[str]]
        if counter % 2 == 0:
            seat_predicate = _is_seat_empty
            change_seat_state = _should_occupy_seat
        else:
            seat_predicate = _is_seat_occupied
            change_seat_state = _should_empty_seat

        # round to occupy some seats
        number_of_modifications = _apply_round(
            seats,
            seat_predicate,
            change_seat_state
        )

        counter += 1

    return _count_occupied_seats(seats)


def _should_occupy_seat(occupied_adjacent_seats: int) -> Optional[str]:
    return "#" if occupied_adjacent_seats == 0 else None


def _should_empty_seat(occupied_adjacent_seats: int) -> Optional[str]:
    return "L" if occupied_adjacent_seats >= 4 else None


def _is_seat_occupied(seat: str) -> bool:
    return seat == OCCUPIED_SEAT


def _is_seat_empty(seat: str) -> bool:
    return seat == EMPTY_SEAT


def _count_occupied_seats(seats: List[List[str]]):
    return sum((_is_seat_occupied(seat) for row in seats for seat in row))


def _apply_round(seats: List[List[str]],
                 seat_predicate: Callable[[str], bool],
                 change_seat_state: Callable[[int], Optional[str]]) -> int:
    seats_snapshot = [list(row) for row in seats]
    width = len(seats_snapshot)
    height = len(seats_snapshot[0])
    change_counter = 0
    for row in range(width):
        for col in range(height):
            if seat_predicate(seats_snapshot[row][col]):
                number_of_occupied_seats = _count_occupied_adjacent_seats(row, col, seats_snapshot)
                new_state = change_seat_state(number_of_occupied_seats)
                if new_state:
                    seats[row][col] = new_state
                    change_counter += 1

    return change_counter


def _count_occupied_adjacent_seats(row: int, col: int, seats: List[List[str]]) -> int:
    return sum([
        _is_occupied(row - 1, col - 1, seats),
        _is_occupied(row - 1, col, seats),
        _is_occupied(row - 1, col + 1, seats),
        _is_occupied(row, col - 1, seats),
        _is_occupied(row, col + 1, seats),
        _is_occupied(row + 1, col - 1, seats),
        _is_occupied(row + 1, col, seats),
        _is_occupied(row + 1, col + 1, seats),
    ])


def _is_occupied(row: int, col: int, seats: List[List[str]]) -> bool:
    if 0 <= row < len(seats):
        if 0 <= col < len(seats[row]):
            return _is_seat_occupied(seats[row][col])

    return False  # out of bounds seat ar not occupied


def _parse(raw_rows: Iterable[str]) -> List[List[str]]:
    return [
        _parse_row(raw_row)
        for raw_row in raw_rows
    ]


def _parse_row(raw_row: str) -> List[str]:
    return [c for c in raw_row.rstrip()]


def _print_seats(seats: List[List[str]]) -> None:
    for row in seats:
        print("".join(row))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        seats_from_file = _parse(file.readlines())

        solution_part1 = fill_seats(seats_from_file)
        print(f"solution (part1): {solution_part1}")
        assert solution_part1 == 2289
