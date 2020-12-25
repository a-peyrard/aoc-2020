from hamcrest import assert_that, equal_to

from aoc.day3.tobogan_trajectory import _parse_line, count_trees_in_trajectory, analyze_trajectories


class TestCountTreesInTrajectory:
    def test_should_validate_given_example(self):
        # GIVEN
        slope = list(map(
            _parse_line,
            [
                "..##.......",
                "#...#...#..",
                ".#....#..#.",
                "..#.#...#.#",
                ".#...##..#.",
                "..#.##.....",
                ".#.#.#....#",
                ".#........#",
                "#.##...#...",
                "#...##....#",
                ".#..#...#.#"
            ]
        ))

        # WHEN
        trees = count_trees_in_trajectory(slope, right=3, down=1)

        # THEN
        assert_that(trees, equal_to(7))

    def test_should_correctly_wrap(self):
        # GIVEN
        slope = list(map(
            _parse_line,
            [
                "....",
                "....",
                "..#."
            ]
        ))

        # WHEN
        trees = count_trees_in_trajectory(slope, right=3, down=1)

        # THEN
        assert_that(trees, equal_to(1))


class TestAnalyzeTrajectories:
    def test_should_validate_part1_example(self):
        # GIVEN
        slope = list(map(
            _parse_line,
            [
                "..##.......",
                "#...#...#..",
                ".#....#..#.",
                "..#.#...#.#",
                ".#...##..#.",
                "..#.##.....",
                ".#.#.#....#",
                ".#........#",
                "#.##...#...",
                "#...##....#",
                ".#..#...#.#"
            ]
        ))

        # WHEN
        trees = analyze_trajectories(slope, [(3, 1)])

        # THEN
        assert_that(trees, equal_to(7))

    def test_should_validate_part2_example(self):
        # GIVEN
        slope = list(map(
            _parse_line,
            [
                "..##.......",
                "#...#...#..",
                ".#....#..#.",
                "..#.#...#.#",
                ".#...##..#.",
                "..#.##.....",
                ".#.#.#....#",
                ".#........#",
                "#.##...#...",
                "#...##....#",
                ".#..#...#.#"
            ]
        ))

        # WHEN
        trees = analyze_trajectories(
            slope,
            [
                (1, 1),
                (3, 1),
                (5, 1),
                (7, 1),
                (1, 2)
            ]
        )

        # THEN
        assert_that(trees, equal_to(336))
