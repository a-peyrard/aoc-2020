from hamcrest import equal_to, assert_that

from aoc.day15.rambunctious_recitation import play_game


class TestPlayGame:
    def test_should_work_with_less_turns_than_starting_numbers(self):
        # GIVEN
        starting_numbers = [0, 3, 6]
        number_of_turns = 3

        # WHEN
        res = play_game(starting_numbers, number_of_turns)

        # THEN
        assert_that(res, equal_to(6))

    def test_should_validate_first_example(self):
        # GIVEN
        starting_numbers = [0, 3, 6]
        number_of_turns = 2020

        # WHEN
        res = play_game(starting_numbers, number_of_turns)

        # THEN
        assert_that(res, equal_to(436))

    def test_should_validate_second_example(self):
        # GIVEN
        starting_numbers = [1, 3, 2]
        number_of_turns = 2020

        # WHEN
        res = play_game(starting_numbers, number_of_turns)

        # THEN
        assert_that(res, equal_to(1))

    def test_should_validate_third_example(self):
        # GIVEN
        starting_numbers = [2, 1, 3]
        number_of_turns = 2020

        # WHEN
        res = play_game(starting_numbers, number_of_turns)

        # THEN
        assert_that(res, equal_to(10))

    def test_should_validate_fourth_example(self):
        # GIVEN
        starting_numbers = [1, 2, 3]
        number_of_turns = 2020

        # WHEN
        res = play_game(starting_numbers, number_of_turns)

        # THEN
        assert_that(res, equal_to(27))

    def test_should_validate_fifth_example(self):
        # GIVEN
        starting_numbers = [2, 3, 1]
        number_of_turns = 2020

        # WHEN
        res = play_game(starting_numbers, number_of_turns)

        # THEN
        assert_that(res, equal_to(78))

    def test_should_validate_sixth_example(self):
        # GIVEN
        starting_numbers = [3, 2, 1]
        number_of_turns = 2020

        # WHEN
        res = play_game(starting_numbers, number_of_turns)

        # THEN
        assert_that(res, equal_to(438))

    def test_should_validate_seventh_example(self):
        # GIVEN
        starting_numbers = [3, 1, 2]
        number_of_turns = 2020

        # WHEN
        res = play_game(starting_numbers, number_of_turns)

        # THEN
        assert_that(res, equal_to(1836))
