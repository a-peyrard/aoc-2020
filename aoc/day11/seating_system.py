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

--- Part Two ---
As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care
about the first seat they can see in each of those eight directions!
Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight
 directions. For example, the empty seat below would see eight occupied seats:
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:
.............
.L.L.#.#.#.#.
.............
The empty seat below would see no occupied seats:
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an
 occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply:
 empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.
Given the same starting layout as above, these new rules cause the seating area to shift around as follows:
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

#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#

#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count
 26 occupied seats.
Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how
 many seats end up occupied?
"""
import os
from typing import List, Iterable, Callable, Optional, Tuple

OCCUPIED_SEAT = "#"
EMPTY_SEAT = "L"
FLOOR = "."


OccupiedPredicate = Callable[[int, int, List[List[str]], Callable[[int, int], Tuple[int, int]]], bool]


def fill_seats(seats: List[List[str]],
               is_occupied_predicate: OccupiedPredicate,
               empty_seat_threshold: int = 4) -> int:
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
            change_seat_state = _should_empty_seat_factory(empty_seat_threshold)

        # round to occupy some seats
        number_of_modifications = _apply_round(
            seats,
            seat_predicate,
            change_seat_state,
            is_occupied_predicate
        )

        counter += 1

    return _count_occupied_seats(seats)


def _should_occupy_seat(occupied_adjacent_seats: int) -> Optional[str]:
    return "#" if occupied_adjacent_seats == 0 else None


def _should_empty_seat_factory(threshold: int) -> Callable[[int], Optional[str]]:
    return lambda occupied_adjacent_seats: "L" if occupied_adjacent_seats >= threshold else None


def _is_seat_occupied(seat: str) -> bool:
    return seat == OCCUPIED_SEAT


def _is_seat_empty(seat: str) -> bool:
    return seat == EMPTY_SEAT


def _is_floor(seat: str) -> bool:
    return seat == FLOOR


def _count_occupied_seats(seats: List[List[str]]):
    return sum((_is_seat_occupied(seat) for row in seats for seat in row))


def _apply_round(seats: List[List[str]],
                 seat_predicate: Callable[[str], bool],
                 change_seat_state: Callable[[int], Optional[str]],
                 is_occupied_predicate: OccupiedPredicate) -> int:
    seats_snapshot = _snapshot_seats(seats)
    width = len(seats_snapshot)
    height = len(seats_snapshot[0])
    change_counter = 0
    for row in range(width):
        for col in range(height):
            if seat_predicate(seats_snapshot[row][col]):
                number_of_occupied_seats = _count_occupied_adjacent_seats(
                    row,
                    col,
                    seats_snapshot,
                    is_occupied_predicate
                )
                new_state = change_seat_state(number_of_occupied_seats)
                if new_state:
                    seats[row][col] = new_state
                    change_counter += 1

    return change_counter


def _count_occupied_adjacent_seats(row: int,
                                   col: int,
                                   seats: List[List[str]],
                                   is_occupied_predicate: OccupiedPredicate) -> int:
    return sum([
        is_occupied_predicate(row, col, seats, lambda r, c: (r - 1, c - 1)),
        is_occupied_predicate(row, col, seats, lambda r, c: (r - 1, c)),
        is_occupied_predicate(row, col, seats, lambda r, c: (r - 1, c + 1)),
        is_occupied_predicate(row, col, seats, lambda r, c: (r, c - 1)),
        is_occupied_predicate(row, col, seats, lambda r, c: (r, c + 1)),
        is_occupied_predicate(row, col, seats, lambda r, c: (r + 1, c - 1)),
        is_occupied_predicate(row, col, seats, lambda r, c: (r + 1, c)),
        is_occupied_predicate(row, col, seats, lambda r, c: (r + 1, c + 1)),
    ])


def _is_occupied(row: int,
                 col: int,
                 seats: List[List[str]],
                 move: Callable[[int, int], Tuple[int, int]]) -> bool:
    next_row, next_col = move(row, col)
    if 0 <= next_row < len(seats):
        if 0 <= next_col < len(seats[next_row]):
            return _is_seat_occupied(seats[next_row][next_col])

    return False  # out of bounds seat ar not occupied


def _is_direction_occupied(row: int,
                           col: int,
                           seats: List[List[str]],
                           move: Callable[[int, int], Tuple[int, int]]) -> bool:
    next_row, next_col = move(row, col)
    if 0 <= next_row < len(seats):
        if 0 <= next_col < len(seats[next_row]):
            seat = seats[next_row][next_col]
            if _is_floor(seat):
                return _is_direction_occupied(next_row, next_col, seats, move)
            else:
                return _is_seat_occupied(seat)

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


def _snapshot_seats(seats: List[List[str]]) -> List[List[str]]:
    return [list(row) for row in seats]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        seats_from_file = _parse(file.readlines())

        solution_part1 = fill_seats(
            _snapshot_seats(seats_from_file),  # because we are mutating the seats
            is_occupied_predicate=_is_occupied
        )
        print(f"solution (part1): {solution_part1}")
        assert solution_part1 == 2289

        solution_part2 = fill_seats(
            _snapshot_seats(seats_from_file),  # because we are mutating the seats
            is_occupied_predicate=_is_direction_occupied,
            empty_seat_threshold=5
        )
        print(f"solution (part2): {solution_part2}")
        assert solution_part2 == 2059
