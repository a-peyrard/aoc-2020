from hamcrest import equal_to, assert_that

from aoc.day23.crab_cups import Cups, generate_labels, play_game, generate_prod_part2
from aoc.util.list import last


class TestCupsParse:
    def test_should_parse_cups(self):
        # GIVEN
        raw_cups = "1234"

        # WHEN
        cups = Cups.parse(raw_cups)

        # THEN
        cup = cups.current
        assert_that(cup, equal_to(1))
        cup = cups.get_next(from_cup=cup)
        assert_that(cup, equal_to(2))
        cup = cups.get_next(from_cup=cup)
        assert_that(cup, equal_to(3))
        cup = cups.get_next(from_cup=cup)
        assert_that(cup, equal_to(4))

    def test_should_parse_cups_and_create_loop(self):
        # GIVEN
        raw_cups = "12"

        # WHEN
        cups = Cups.parse(raw_cups)

        # THEN
        cup = cups.current
        assert_that(cup, equal_to(1))
        cup = cups.get_next(from_cup=cup)
        assert_that(cup, equal_to(2))
        cup = cups.get_next(from_cup=cup)
        assert_that(cup, equal_to(1))

    def test_should_parse_cups_and_add_additional_cups(self):
        # GIVEN
        raw_cups = "12"

        # WHEN
        cups = Cups.parse(raw_cups, cups_wanted=10)

        # THEN
        assert_that(
            cups.__repr__(),
            equal_to("1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
        )


class TestCupsRepr:
    def test_should_stringify_cups(self):
        # GIVEN
        raw_cups = "1234"

        # WHEN
        cups = Cups.parse(raw_cups)

        # THEN
        assert_that(cups.__repr__(), equal_to("1, 2, 3, 4"))


class TestGenerateLabels:
    def test_should_generate_labels(self):
        # GIVEN
        raw_cups = "3418"
        cups = Cups.parse(raw_cups)

        # WHEN
        labels = generate_labels(cups)

        # THEN
        assert_that(labels, equal_to("834"))


class TestPlayGame:
    def test_should_validate_given_example_with_10_iterations(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups.parse(raw_cups)

        # WHEN
        cups = play_game(cups, iterations=10)

        # THEN
        assert_that(
            generate_labels(cups),
            equal_to("92658374")
        )

    def test_should_validate_given_example_with_100_iterations(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups.parse(raw_cups)

        # WHEN
        cups = play_game(cups, iterations=100)

        # THEN
        assert_that(
            generate_labels(cups),
            equal_to("67384529")
        )

    def test_should_validate_part2_given_example_with_10000000_iterations(self):
        pass  # too slow...
        # # GIVEN
        # raw_cups = "389125467"
        # cups = Cups.parse(raw_cups, cups_wanted=1000000)
        #
        # # WHEN
        # cups = play_game(cups, iterations=10000000)
        #
        # # THEN
        # assert_that(
        #     generate_prod_part2(cups),
        #     equal_to(149245887792)
        # )


class TestCupsMoveToNextCup:
    def test_should_move_to_next_cup(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups.parse(raw_cups)

        # WHEN
        current = cups.move_to_next_cup().current

        # THEN
        assert_that(current, equal_to(8))


class TestCupsCut:
    def test_should_cut_some_cups(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups.parse(raw_cups)
        next_cup1 = cups.get_next()
        next_cup2 = cups.get_next(from_cup=next_cup1)
        next_cup3 = cups.get_next(from_cup=next_cup2)

        # WHEN
        cups.cut(to_cup=next_cup3)

        # THEN
        assert_that(
            cups.__repr__(),
            equal_to("3, 2, 5, 4, 6, 7")
        )


class TestCupsInsertAfter:
    def test_should_insert_after_current_cup(self):
        # GIVEN
        raw_cups = "4123987"
        cups = Cups.parse(raw_cups)
        next_cup1 = cups.get_next()
        next_cup2 = cups.get_next(from_cup=next_cup1)
        next_cup3 = cups.get_next(from_cup=next_cup2)
        cups.cut(to_cup=next_cup3)

        # WHEN
        cups.insert_after(
            target_cup=8,
            start_chain=next_cup1,
            end_chain=next_cup3
        )

        # THEN
        assert_that(
            cups.__repr__(),
            equal_to("4, 9, 8, 1, 2, 3, 7")
        )


class TestCupsGetLowerCup:
    def test_should_get_lower_cup(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups.parse(raw_cups)

        # WHEN
        lower_cup = cups.get_lower_cup(3, disallowed_cup_values=set())

        # THEN
        assert_that(lower_cup, equal_to(2))

    def test_should_get_lower_cup_but_not_disallowed_values(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups.parse(raw_cups)

        # WHEN
        lower_cup = cups.get_lower_cup(9, disallowed_cup_values={8, 7, 6})

        # THEN
        assert_that(lower_cup, equal_to(5))

    def test_should_get_higher_cup_if_no_lower_cup_available(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups.parse(raw_cups)

        # WHEN
        lower_cup = cups.get_lower_cup(3, disallowed_cup_values={5, 2, 1, 9})

        # THEN
        assert_that(lower_cup, equal_to(8))
