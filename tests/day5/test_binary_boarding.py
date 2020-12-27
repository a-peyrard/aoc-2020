from hamcrest import equal_to, assert_that

from aoc.day5.binary_boarding import Seat, calculate_seat_id, get_seat_from_boarding_pass, find_missing_seat


class TestCalculateSeatId:
    def test_should_validate_given_example(self):
        # GIVEN
        seat = Seat(row=44, column=5)

        # WHEN
        seat_id = calculate_seat_id(seat)

        # THEN
        assert_that(seat_id, equal_to(357))


class TestGetSeatFromBoardingPass:
    def test_should_validate_first_example(self):
        # GIVEN
        boarding_pass = "FBFBBFFRLR"

        # WHEN
        row, column = get_seat_from_boarding_pass(boarding_pass)

        # THEN
        assert_that(row, equal_to(44))
        assert_that(column, equal_to(5))

    def test_should_validate_second_example(self):
        # GIVEN
        boarding_pass = "BFFFBBFRRR"

        # WHEN
        row, column = get_seat_from_boarding_pass(boarding_pass)

        # THEN
        assert_that(row, equal_to(70))
        assert_that(column, equal_to(7))

    def test_should_validate_third_example(self):
        # GIVEN
        boarding_pass = "FFFBBBFRRR"

        # WHEN
        row, column = get_seat_from_boarding_pass(boarding_pass)

        # THEN
        assert_that(row, equal_to(14))
        assert_that(column, equal_to(7))

    def test_should_validate_fourth_example(self):
        # GIVEN
        boarding_pass = "BBFFBBFRLL"

        # WHEN
        row, column = get_seat_from_boarding_pass(boarding_pass)

        # THEN
        assert_that(row, equal_to(102))
        assert_that(column, equal_to(4))


class TestFindMissingSeat:
    def test_should_find_missing_id(self):
        # GIVEN
        seat_ids = [5, 6, 8, 9]

        # WHEN
        seat_id = find_missing_seat(seat_ids)

        # THEN
        assert_that(seat_id, equal_to(7))
