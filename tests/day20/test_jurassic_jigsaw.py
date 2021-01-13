from hamcrest import assert_that, contains_exactly

from aoc.day20.jurassic_jigsaw import _parse, Tile


class TestParse:
    def test_should_parse_a_tile(self):
        # GIVEN
        a_tile = """Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##."""

        # WHEN
        tiles = _parse(a_tile.splitlines(keepends=True))

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            tiles,
            contains_exactly(
                Tile(
                    id=2729,
                    top=int("0001010101", 2),
                    right=int("1001000000", 2),
                    bottom=int("1011000110", 2),
                    left=int("0100001111", 2),
                )
            )
        )

    def test_should_parse_multiple_tiles(self):
        # GIVEN
        a_tile = """Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#."""

        # WHEN
        tiles = _parse(a_tile.splitlines(keepends=True))

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            tiles,
            contains_exactly(
                Tile(
                    id=2729,
                    top=int("0001010101", 2),
                    right=int("1001000000", 2),
                    bottom=int("1011000110", 2),
                    left=int("0100001111", 2)
                ),
                Tile(
                    id=2473,
                    top=int("1000011110", 2),
                    right=int("0001110100", 2),
                    bottom=int("0011101010", 2),
                    left=int("1111000110", 2)
                )
            )
        )
