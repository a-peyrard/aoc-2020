from hamcrest import equal_to, assert_that, contains_exactly

from aoc.day23.crab_cups import Cup, Cups


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

