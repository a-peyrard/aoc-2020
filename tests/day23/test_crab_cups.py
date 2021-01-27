from hamcrest import equal_to, assert_that, contains_exactly

from aoc.day23.crab_cups import Cup, Cups, generate_labels, play_game, generate_prod_part2
from aoc.util.list import last


class TestCupParse:
    def test_should_parse_cups(self):
        # GIVEN
        raw_cups = "1234"

        # WHEN
        cup = Cup.parse(raw_cups)

        # THEN
        assert_that(cup.value, equal_to(1))
        cup = cup.next
        assert_that(cup.value, equal_to(2))
        cup = cup.next
        assert_that(cup.value, equal_to(3))
        cup = cup.next
        assert_that(cup.value, equal_to(4))

    def test_should_parse_cups_and_create_loop(self):
        # GIVEN
        raw_cups = "12"

        # WHEN
        original_cup = Cup.parse(raw_cups)

        # THEN
        assert_that(original_cup.value, equal_to(1))
        cup = original_cup.next
        assert_that(cup.value, equal_to(2))
        cup = cup.next
        assert_that(cup.value, equal_to(1))
        assert_that(cup == original_cup, equal_to(True))

    def test_should_parse_cups_and_add_additional_cups(self):
        # GIVEN
        raw_cups = "12"

        # WHEN
        original_cup = Cup.parse(raw_cups, cups_wanted=10)

        # THEN
        assert_that(
            original_cup.__repr__(),
            equal_to("1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
        )


class TestCupRepr:
    def test_should_stringify_cups(self):
        # GIVEN
        raw_cups = "1234"

        # WHEN
        cup = Cup.parse(raw_cups)

        # THEN
        assert_that(cup.__repr__(), equal_to("1, 2, 3, 4"))


class TestCupNextCup:
    def test_should_get_next_cup(self):
        # GIVEN
        raw_cups = "1234"
        cup = Cup.parse(raw_cups)

        # WHEN
        next_cup = cup.next_cup()

        # THEN
        assert_that(next_cup.value, equal_to(2))

    def test_should_allow_to_specify_distance(self):
        # GIVEN
        raw_cups = "389125467"
        cup = Cup.parse(raw_cups)

        # WHEN
        cup_distance_3 = cup.next_cup(distance=3)

        # THEN
        assert_that(cup_distance_3.value, equal_to(2))


class TestCupsInit:
    def test_should_init_cups(self):
        # GIVEN
        raw_cups = "3418"
        cup = Cup.parse(raw_cups)
        cup_3 = cup
        cup_4 = cup_3.next
        cup_1 = cup_4.next
        cup_8 = cup_1.next

        # WHEN
        cups = Cups(cup)

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            cups._ordered_cups,
            contains_exactly(
                cup_8, cup_4, cup_3, cup_1
            )
        )
        assert_that(
            cups._lookup,
            equal_to({
                8: 0,
                4: 1,
                3: 2,
                1: 3
            })
        )


class TestGenerateLabels:
    def test_should_generate_labels(self):
        # GIVEN
        raw_cups = "3418"
        cups = Cups(Cup.parse(raw_cups))

        # WHEN
        labels = generate_labels(cups)

        # THEN
        assert_that(labels, equal_to("834"))


class TestPlayGame:
    def test_should_validate_given_example_with_10_iterations(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups(Cup.parse(raw_cups))

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
        cups = Cups(Cup.parse(raw_cups))

        # WHEN
        cups = play_game(cups, iterations=100)

        # THEN
        assert_that(
            generate_labels(cups),
            equal_to("67384529")
        )

    def test_should_validate_part2_given_example_with_10000000_iterations(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups(Cup.parse(raw_cups, cups_wanted=1000000))

        # WHEN
        cups = play_game(cups, iterations=10000000)

        # THEN
        assert_that(
            generate_prod_part2(cups),
            equal_to(149245887792)
        )


class TestCupsMoveToNextCup:
    def test_should_move_to_next_cup(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups(Cup.parse(raw_cups))

        # WHEN
        current = cups.move_to_next_cup().current_cup

        # THEN
        assert_that(current.value, equal_to(8))


class TestCupCut:
    def test_should_cut_some_cups(self):
        # GIVEN
        raw_cups = "389125467"
        cup = Cup.parse(raw_cups)
        next_cup1 = cup.next
        next_cup2 = next_cup1.next
        next_cup3 = next_cup2.next

        # WHEN
        cup.cut(to_cup=next_cup3)

        # THEN
        assert_that(
            cup.__repr__(),
            equal_to("3, 2, 5, 4, 6, 7")
        )


class TestCupInsertAfter:
    def test_should_insert_after_current_cup(self):
        # GIVEN
        raw_cups = "4987"
        cup = Cup.parse(raw_cups)

        cup_to_insert = Cup.parse("123")
        last_cup_to_insert = last(cup_to_insert.iter(), default_value=cup_to_insert)

        # WHEN
        cup.insert_after(
            start_chain=cup_to_insert,
            end_chain=last_cup_to_insert
        )

        # THEN
        assert_that(
            cup.__repr__(),
            equal_to("4, 1, 2, 3, 9, 8, 7")
        )


class TestCupsGetLowerCup:
    def test_should_get_lower_cup(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups(Cup.parse(raw_cups))

        # WHEN
        lower_cup = cups.get_lower_cup(3, disallowed_cup_values=set())

        # THEN
        assert_that(lower_cup.value, equal_to(2))

    def test_should_get_lower_cup_but_not_disallowed_values(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups(Cup.parse(raw_cups))

        # WHEN
        lower_cup = cups.get_lower_cup(9, disallowed_cup_values={8, 7, 6})

        # THEN
        assert_that(lower_cup.value, equal_to(5))

    def test_should_get_higher_cup_if_no_lower_cup_available(self):
        # GIVEN
        raw_cups = "389125467"
        cups = Cups(Cup.parse(raw_cups))

        # WHEN
        lower_cup = cups.get_lower_cup(3, disallowed_cup_values={5, 2, 1, 9})

        # THEN
        assert_that(lower_cup.value, equal_to(8))
