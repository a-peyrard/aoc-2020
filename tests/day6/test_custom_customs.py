from hamcrest import assert_that, equal_to

from aoc.day6.custom_customs import _count_answers_in_group, count_in_groups, _count_same_answers_in_group


class TestCountInGroups:
    def test_should_validate_the_given_part1_example(self):
        # GIVEN
        lines = """abc

a
b
c

ab
ac

a
a
a
a

b"""

        # WHEN
        res = count_in_groups(
            lines.splitlines(keepends=True),
            _count_answers_in_group
        )

        # THEN
        assert_that(res, equal_to(11))

    def test_should_validate_the_given_part2_example(self):
        # GIVEN
        lines = """abc

a
b
c

ab
ac

a
a
a
a

b"""

        # WHEN
        res = count_in_groups(
            lines.splitlines(keepends=True),
            _count_same_answers_in_group
        )

        # THEN
        assert_that(res, equal_to(6))


class TestCountAnswersInGroup:
    def test_should_validate_the_first_group(self):
        # GIVEN
        group = [
            "abc"
        ]

        # WHEN
        res = _count_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(3))

    def test_should_validate_the_second_group(self):
        # GIVEN
        group = [
            "a",
            "b",
            "c"
        ]

        # WHEN
        res = _count_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(3))

    def test_should_validate_the_third_group(self):
        # GIVEN
        group = [
            "ab",
            "ac"
        ]

        # WHEN
        res = _count_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(3))

    def test_should_validate_the_fourth_group(self):
        # GIVEN
        group = [
            "a",
            "a",
            "a",
            "a",
        ]

        # WHEN
        res = _count_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(1))

    def test_should_validate_the_fifth_group(self):
        # GIVEN
        group = [
            "b"
        ]

        # WHEN
        res = _count_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(1))


class TestCountSameAnswersInGroup:
    def test_should_validate_the_first_group(self):
        # GIVEN
        group = [
            "abc"
        ]

        # WHEN
        res = _count_same_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(3))

    def test_should_validate_the_second_group(self):
        # GIVEN
        group = [
            "a",
            "b",
            "c"
        ]

        # WHEN
        res = _count_same_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(0))

    def test_should_validate_the_third_group(self):
        # GIVEN
        group = [
            "ab",
            "ac"
        ]

        # WHEN
        res = _count_same_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(1))

    def test_should_validate_the_fourth_group(self):
        # GIVEN
        group = [
            "a",
            "a",
            "a",
            "a",
        ]

        # WHEN
        res = _count_same_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(1))

    def test_should_validate_the_fifth_group(self):
        # GIVEN
        group = [
            "b"
        ]

        # WHEN
        res = _count_same_answers_in_group(group)

        # THEN
        assert_that(res, equal_to(1))
