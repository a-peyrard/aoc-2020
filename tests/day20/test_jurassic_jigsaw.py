from unittest.mock import ANY

from hamcrest import assert_that, contains_exactly, equal_to, contains_inanyorder

from aoc.day20.jurassic_jigsaw import Tile, _reverse_binary, _parse, solve_part1, Direction, _find_corners, _flip_mut, \
    _rotate_mut
from aoc.util.num import binary_to_string


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
                    inner_content=[
                        ["#", "#", "#", ".", "#", ".", ".", "."],
                        [".", "#", ".", "#", ".", ".", ".", "."],
                        [".", ".", ".", "#", ".", ".", "#", "."],
                        ["#", "#", ".", ".", "#", "#", ".", "#"],
                        ["#", ".", "#", "#", "#", "#", ".", "."],
                        ["#", "#", "#", ".", "#", ".", "#", "."],
                        ["#", ".", "#", "#", "#", "#", ".", "."],
                        ["#", ".", ".", "#", ".", "#", "#", "."],
                    ],
                    flipped=False,
                    rotation=0
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
                    left=int("0100001111", 2),
                    inner_content=ANY
                ),
                Tile(
                    id=2473,
                    top=int("1000011110", 2),
                    right=int("0001110100", 2),
                    bottom=int("0011101010", 2),
                    left=int("1111000110", 2),
                    inner_content=ANY
                )
            )
        )


class TestTileDraw:
    def test_should_draw_a_tile(self):
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
        tile, = _parse(a_tile.splitlines(keepends=True))
        _, flipped_rotation_180, _ = tile.flip().rotate()

        # WHEN
        drawing = flipped_rotation_180.draw()

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            drawing,
            equal_to([
                [".", ".", ".", "#", ".", "#", "#", "#"], 
                [".", ".", ".", ".", "#", ".", "#", "."], 
                [".", "#", ".", ".", "#", ".", ".", "."], 
                ["#", ".", "#", "#", ".", ".", "#", "#"], 
                [".", ".", "#", "#", "#", "#", ".", "#"], 
                [".", "#", ".", "#", ".", "#", "#", "#"], 
                [".", ".", "#", "#", "#", "#", ".", "#"], 
                [".", "#", "#", ".", "#", ".", ".", "#"]
            ])
        )

    def test_should_draw_a_flipped_r180_custom_tile(self):
        # GIVEN
        tile = Tile(
            id=123,
            top=123,
            right=123,
            bottom=123,
            left=123,
            inner_content=[
                ["1", "2", "3", "4"],
                ["5", "6", "7", "8"],
                ["9", "10", "11", "12"],
                ["13", "14", "15", "16"]
            ]
        )
        _, flipped_rotation_180, _ = tile.flip().rotate()

        # WHEN
        drawing = flipped_rotation_180.draw()

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            drawing,
            equal_to([
                ["4", "3", "2", "1"],
                ["8", "7", "6", "5"],
                ["12", "11", "10", "9"],
                ["16", "15", "14", "13"]
            ])
        )

    def test_should_draw_a_flipped_custom_tile(self):
        # GIVEN
        tile = Tile(
            id=123,
            top=123,
            right=123,
            bottom=123,
            left=123,
            inner_content=[
                ["1", "2", "3", "4"],
                ["5", "6", "7", "8"],
                ["9", "10", "11", "12"],
                ["13", "14", "15", "16"]
            ]
        )
        flipped = tile.flip()

        # WHEN
        drawing = flipped.draw()

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            drawing,
            equal_to([
                ["13", "14", "15", "16"],
                ["9", "10", "11", "12"],
                ["5", "6", "7", "8"],
                ["1", "2", "3", "4"],
            ])
        )


class TestTileMatch:
    def test_should_match_with_270_rotation(self):
        # GIVEN
        tile_3079 = Tile.parse("""Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...""".splitlines())
        tile_2473 = Tile.parse("""Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.""".splitlines())
        tile_2473_flip_then_rotate270 = tile_2473.flip()\
            ._rotate_90()\
            ._rotate_90()\
            ._rotate_90()

        # WHEN
        matches = tile_3079.match(tile_2473_flip_then_rotate270)

        # THEN
        assert_that(
            matches,
            equal_to([
                Direction.BOTTOM
            ])
        )


class TestReverseBinary:
    def test_should_reverse_binary(self):
        # GIVEN
        orig = "1010000000"

        # WHEN
        res = _reverse_binary(int(orig, 2), 10)

        # THEN
        assert_that(
            binary_to_string(res, size=10),
            equal_to("0000000101")
        )

    def test_should_reverse_another_binary(self):
        # GIVEN
        orig = "0110001101"

        # WHEN
        res = _reverse_binary(int(orig, 2), 10)

        # THEN
        assert_that(
            binary_to_string(res, size=10),
            equal_to("1011000110")
        )


class TestTileRotate:
    def test_should_rotate_tile_by_90_degree(self):
        # GIVEN
        a_tile = Tile.parse(
            """Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.""".splitlines()
        )

        # WHEN
        rotate90 = a_tile._rotate_90()

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            rotate90,
            equal_to(
                Tile(
                    id=2729,
                    top=int("1111000010", 2),
                    right=int("0001010101", 2),
                    bottom=int("0000001001", 2),
                    left=int("1011000110", 2),
                    inner_content=ANY,
                    flipped=False,
                    rotation=90
                )
            )
        )

    def test_should_rotate(self):
        # GIVEN
        a_tile = Tile.parse(
            """Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.""".splitlines()
        )

        # WHEN
        rotations = a_tile.rotate()

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            rotations,
            contains_inanyorder(
                Tile(
                    id=2729,
                    top=int("1111000010", 2),
                    right=int("0001010101", 2),
                    bottom=int("0000001001", 2),
                    left=int("1011000110", 2),
                    inner_content=ANY,
                    flipped=False,
                    rotation=90
                ),
                Tile(
                    id=2729,
                    top=int("0110001101", 2),
                    right=int("1111000010", 2),
                    bottom=int("1010101000", 2),
                    left=int("0000001001", 2),
                    inner_content=ANY,
                    flipped=False,
                    rotation=180
                ),
                Tile(
                    id=2729,
                    top=int("1001000000", 2),
                    right=int("0110001101", 2),
                    bottom=int("0100001111", 2),
                    left=int("1010101000", 2),
                    inner_content=ANY,
                    flipped=False,
                    rotation=270
                )
            )
        )


class TestTileFlip:
    def test_should_flip(self):
        # GIVEN
        a_tile = Tile.parse(
            """Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.""".splitlines()
        )

        # WHEN
        flip_y = a_tile.flip()

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            flip_y,
            equal_to(
                Tile(
                    id=2729,
                    top=int("1011000110", 2),
                    right=int("0000001001", 2),
                    bottom=int("0001010101", 2),
                    left=int("1111000010", 2),
                    inner_content=ANY,
                    flipped=True,
                    rotation=0
                )
            )
        )


class TestFindCorners:
    def test_should_find_corners_in_the_given_jigsaw(self):
        # GIVEN
        raw_tiles = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

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
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
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

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""
        tiles_by_id = {
            tile.id: tile
            for tile in _parse(raw_tiles.splitlines(keepends=True))
        }

        # WHEN
        corners = _find_corners(
            tiles_by_id
        )

        # THEN
        assert_that(
            corners,
            contains_inanyorder(
                1951,
                3079,
                2971,
                1171
            )
        )


class TestFlipMut:
    def test_should_flip_a_simple_matrix(self):
        # GIVEN
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

        # WHEN
        res = _flip_mut(matrix)

        # THEN
        assert_that(
            res,
            equal_to([
                [7, 8, 9],
                [4, 5, 6],
                [1, 2, 3]
            ])
        )

    def test_should_flip_a_tile_matrix(self):
        # GIVEN
        matrix = [
            ["#", ".", ".", "#", ".", ".", ".", "."],
            [".", ".", ".", "#", "#", ".", ".", "#"],
            ["#", "#", "#", ".", "#", ".", ".", "."],
            ["#", ".", "#", "#", ".", "#", "#", "#"],
            ["#", ".", ".", ".", "#", ".", "#", "#"],
            ["#", ".", "#", ".", "#", ".", ".", "#"],
            [".", "#", ".", ".", ".", ".", "#", "."],
            ["#", "#", ".", ".", ".", "#", ".", "#"],
        ]

        # WHEN
        res = _flip_mut(matrix)

        # THEN
        assert_that(
            res,
            equal_to([
                ["#", "#", ".", ".", ".", "#", ".", "#"],
                [".", "#", ".", ".", ".", ".", "#", "."],
                ["#", ".", "#", ".", "#", ".", ".", "#"],
                ["#", ".", ".", ".", "#", ".", "#", "#"],
                ["#", ".", "#", "#", ".", "#", "#", "#"],
                ["#", "#", "#", ".", "#", ".", ".", "."],
                [".", ".", ".", "#", "#", ".", ".", "#"],
                ["#", ".", ".", "#", ".", ".", ".", "."],
            ])
        )


class TestRotateMut:
    def test_should_rotate_a_matrix(self):
        # GIVEN
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

        # WHEN
        res = _rotate_mut(matrix)

        # THEN
        assert_that(
            res,
            equal_to([
                [7, 4, 1],
                [8, 5, 2],
                [9, 6, 3]
            ])
        )

    def test_should_rotate_a_bigger_matrix(self):
        # GIVEN
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]

        # WHEN
        res = _rotate_mut(matrix)

        # THEN
        assert_that(
            res,
            equal_to([
                [13, 9, 5, 1],
                [14, 10, 6, 2],
                [15, 11, 7, 3],
                [16, 12, 8, 4],
            ])
        )

    def test_should_rotate_a_small_matrix(self):
        # GIVEN
        matrix = [
            [1, 2],
            [3, 4],
        ]

        # WHEN
        res = _rotate_mut(matrix)

        # THEN
        assert_that(
            res,
            equal_to([
                [3, 1],
                [4, 2],
            ])
        )

    def test_should_rotate_a_big_matrix(self):
        # GIVEN
        matrix = [
            [1, 7, 13, 19, 25, 31],
            [2, 8, 14, 20, 26, 32],
            [3, 9, 15, 21, 27, 33],
            [4, 10, 16, 22, 28, 34],
            [5, 11, 17, 23, 29, 35],
            [6, 12, 18, 24, 30, 36]
        ]

        # WHEN
        res = _rotate_mut(matrix)

        # THEN
        assert_that(
            res,
            equal_to([
                [6, 5, 4, 3, 2, 1],
                [12, 11, 10, 9, 8, 7],
                [18, 17, 16, 15, 14, 13],
                [24, 23, 22, 21, 20, 19],
                [30, 29, 28, 27, 26, 25],
                [36, 35, 34, 33, 32, 31]
            ])
        )


class TestSolvePart1:
    def test_should_do_the_given_jigsaw(self):
        # GIVEN
        raw_tiles = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

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
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
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

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

        # WHEN
        res = solve_part1(
            _parse(raw_tiles.splitlines(keepends=True))
        )

        # THEN
        assert_that(res, equal_to(20899048083289))
