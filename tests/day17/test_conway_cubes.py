from hamcrest import assert_that, equal_to

from aoc.day17.conway_cubes import _parse, _print_pocket_dimension, count_active, _count_active_neighbors, \
    execute_cycle, _transform_pocket_to_ints, solve_part1


class TestParse:
    def test_should_parse_given_example(self):
        # GIVEN
        raw = """.#.
..#
###"""

        # WHEN
        pocket = _parse(raw.splitlines(keepends=True), 6)

        # THEN
        _print_pocket_dimension(pocket)


class TestCountActive:
    def test_should_count_for_initial_state(self):
        # GIVEN
        raw = """.#.
..#
###"""
        pocket = _parse(raw.splitlines(keepends=True), 6)

        # WHEN
        actives = count_active(pocket)

        # THEN
        assert_that(
            actives,
            equal_to(5)
        )


class TestCountActiveNeighbors:
    def test_should_count_active_neighbors_in_pocket_of_3_by_3(self):
        # GIVEN
        pocket = [
            [
                [True, False, True],
                [True, False, False],
                [False, False, True]
            ],
            [
                [False, False, False],
                [False, True, False],
                [False, False, False]
            ],
            [
                [True, False, False],
                [False, False, True],
                [True, True, True]
            ]
        ]

        # WHEN
        actives = _count_active_neighbors(
            coord=(1, 1, 1),
            pocket=pocket
        )

        # THEN
        assert_that(
            actives,
            equal_to(9)
        )


class TestTransformPocketToInts:
    def test_should_transform_bool_to_ints(self):
        # GIVEN
        pocket = [
            [
                [True, False, True],
                [True, False, False],
                [False, False, True]
            ],
            [
                [False, False, False],
                [False, True, False],
                [False, False, False]
            ],
            [
                [True, False, False],
                [False, False, True],
                [True, True, True]
            ]
        ]

        # WHEN
        ints_pocket = _transform_pocket_to_ints(pocket)

        # THEN
        assert_that(
            ints_pocket,
            equal_to([
                [
                    [1, 0, 1],
                    [1, 0, 0],
                    [0, 0, 1]
                ],
                [
                    [0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]
                ],
                [
                    [1, 0, 0],
                    [0, 0, 1],
                    [1, 1, 1]
                ]
            ])
        )


class TestExecuteCycle:
    def test_should_execute_a_cycle(self):
        # GIVEN
        raw = """.#.
..#
###"""
        pocket = _parse(raw.splitlines(keepends=True), 1)

        # WHEN
        new_pocket = execute_cycle(0, 1, pocket)

        # THEN
        assert_that(
            _transform_pocket_to_ints(new_pocket),
            equal_to([
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 1, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0]
                ]
            ])
        )


class TestSolvePart1:
    def test_should_solve_given_example(self):
        # GIVEN
        raw = """.#.
..#
###"""

        # WHEN
        actives = solve_part1(raw.splitlines(keepends=True), 6)

        # THEN
        assert_that(
            actives,
            equal_to(112)
        )
