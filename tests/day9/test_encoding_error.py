from hamcrest import equal_to, assert_that

from aoc.day9.encoding_error import analyze_numbers, Preamble


class TestPreamble:
    def test_should_find_sum(self):
        # GIVEN
        preamble = Preamble(initial=[1, 2, 3, 4, 5, 6])

        # WHEN
        res = preamble.can_sum(7)

        # THEN
        assert_that(res, equal_to(True))

    def test_should_not_find_sum(self):
        # GIVEN
        preamble = Preamble(initial=[1, 2, 3, 4, 5, 6])

        # WHEN
        res = preamble.can_sum(70)

        # THEN
        assert_that(res, equal_to(False))

    def test_should_update_preamble_and_find_sum(self):
        # GIVEN
        preamble = Preamble(initial=[1, 2, 3, 4, 5, 6])

        # WHEN
        preamble.update(add=68, remove=3)
        res = preamble.can_sum(70)

        # THEN
        assert_that(res, equal_to(True))

    def test_should_update_preamble_and_not_find_sum(self):
        # GIVEN
        preamble = Preamble(initial=[1, 2, 3, 4, 5, 6])

        # WHEN
        preamble.update(add=68, remove=2)
        res = preamble.can_sum(70)

        # THEN
        assert_that(res, equal_to(False))


class TestAnalyzeNumbers:
    def test_should_validate_given_example(self):
        # GIVEN
        raw_numbers = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

        # WHEN
        res = analyze_numbers(
            numbers=list(map(int, raw_numbers.splitlines(keepends=True))),
            preamble_size=5
        )

        # THEN
        assert_that(res, equal_to(127))
