from hamcrest import assert_that, equal_to

from aoc.day17.conway_cubes_part2 import solve_part2


class TestSolvePart2:
    def test_should_solve_given_example(self):
        # GIVEN
        raw = """.#.
..#
###"""

        # WHEN
        actives = solve_part2(raw.splitlines(keepends=True), 6)

        # THEN
        assert_that(
            actives,
            equal_to(848)
        )
