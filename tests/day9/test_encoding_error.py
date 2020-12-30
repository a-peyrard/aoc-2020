from hamcrest import equal_to, assert_that

from aoc.day9.encoding_error import analyze_numbers, Preamble, find_contiguous_set, generate_solution_part2


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


class TestFindContiguousSet:
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
        res = find_contiguous_set(
            numbers=list(map(int, raw_numbers.splitlines(keepends=True))),
            target=127
        )

        # THEN
        assert_that(res, equal_to([15, 25, 47, 40]))

    def test_should_validate_set_at_the_end(self):
        # GIVEN
        numbers = [1, 2, 3, 4, 18]

        # WHEN
        res = find_contiguous_set(
            numbers=numbers,
            target=22
        )

        # THEN
        assert_that(res, equal_to([4, 18]))

    def test_should_shrink_the_buffer(self):
        # GIVEN
        numbers = [35, 2, 3, 4]

        # WHEN
        res = find_contiguous_set(
            numbers=numbers,
            target=5
        )

        # THEN
        assert_that(res, equal_to([2, 3]))


class TestGenerateSolutionPart2:
    def test_should_validate_given_example(self):
        # GIVEN
        contiguous_set = [15, 25, 47, 40]

        # WHEN
        res = generate_solution_part2(contiguous_set)

        # THEN
        assert_that(res, equal_to(62))
