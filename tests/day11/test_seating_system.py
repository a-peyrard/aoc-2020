from hamcrest import assert_that, equal_to

from aoc.day11.seating_system import fill_seats, _parse, _is_occupied, _is_direction_occupied


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
        res = fill_seats(
            _parse(raw_seats.splitlines(keepends=True)),
            is_occupied_predicate=_is_occupied
        )

        # THEN
        assert_that(res, equal_to(37))

    def test_should_validate_part2_example(self):
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
        res = fill_seats(
            _parse(raw_seats.splitlines(keepends=True)),
            is_occupied_predicate=_is_direction_occupied,
            empty_seat_threshold=5
        )

        # THEN
        assert_that(res, equal_to(26))
