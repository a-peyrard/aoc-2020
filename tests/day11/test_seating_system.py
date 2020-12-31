import os

from hamcrest import assert_that, equal_to

from aoc.day11.seating_system import fill_seats, _parse


class TestFillSeats:
    def test_should_validate_first_example(self):
        # GIVEN
        raw_seats = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

        # WHEN
        res = fill_seats(_parse(raw_seats.splitlines(keepends=True)))

        # THEN
        assert_that(res, equal_to(37))
