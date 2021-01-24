import time
from copy import deepcopy
from unittest.mock import ANY

from hamcrest import assert_that, contains_exactly, equal_to, contains_inanyorder, any_of

from aoc.day20.jurassic_jigsaw import Tile, _reverse_binary, _parse, solve_part1, Direction, _find_corners, _flip_mut, \
    _rotate_mut, _draw_picture, Pattern, _get_next_coordinates, _do_jigsaw, _can_use_tile, _generate_empty_jigsaw, \
    solve_part2
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


class TestTileDrawing:
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
        drawing = flipped_rotation_180.drawing

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
        drawing = flipped_rotation_180.drawing

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
        drawing = flipped.drawing

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

    def test_should_draw_a_flipped_custom_tile_with_rotation_at_270(self):
        # GIVEN
        tile_c = Tile(
            id=123,
            top=123,
            right=123,
            bottom=123,
            left=123,
            inner_content=[
                ["1", "2"],
                ["3", "4"]
            ]
        )

        _, _, tile_c_f_r270 = tile_c.flip().rotate()

        # WHEN
        drawing = tile_c_f_r270.drawing

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            drawing,
            equal_to([
                ["4", "2"],
                ["3", "1"]
            ])
        )

    def test_should_draw_a_flipped_tile_with_rotation_at_270(self):
        # GIVEN
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

        _, _, tile_2473_f_r270 = tile_2473.flip().rotate()

        # WHEN
        drawing = tile_2473_f_r270.drawing

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            "\n".join((
                "".join(row)
                for row in drawing
            )),
            equal_to("""#.##....
.#.###..
##.#..##
######.#
.#.#.#..
.###.###
.###.##.
######..""")
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
            list(matches),
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
        # noinspection PyTypeChecker
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
        res, corners = solve_part1(
            _parse(raw_tiles.splitlines(keepends=True))
        )

        # THEN
        assert_that(res, equal_to(20899048083289))
        # noinspection PyTypeChecker
        assert_that(
            corners,
            contains_inanyorder(
                1951,
                3079,
                2971,
                1171
            )
        )


class TestDrawPicture:
    def test_should_draw_the_picture(self):
        # GIVEN
        tile_1 = Tile(
            id=1,
            top=1,
            right=1,
            bottom=1,
            left=1,
            inner_content=[
                ["1", "2"],
                ["3", "4"]
            ]
        )
        tile_2 = Tile(
            id=2,
            top=2,
            right=2,
            bottom=2,
            left=2,
            inner_content=[
                ["5", "6"],
                ["7", "8"]
            ]
        )
        tile_3 = Tile(
            id=3,
            top=3,
            right=3,
            bottom=3,
            left=3,
            inner_content=[
                ["9", "a"],
                ["b", "c"]
            ]
        )
        tile_4 = Tile(
            id=4,
            top=4,
            right=4,
            bottom=4,
            left=4,
            inner_content=[
                ["d", "e"],
                ["f", "g"]
            ]
        )
        jigsaw = [
            [tile_1, tile_2],
            [tile_3, tile_4],
        ]

        # WHEN
        drawing = _draw_picture(jigsaw)

        # THEN
        assert_that(
            drawing,
            equal_to([
                ["1", "2", "5", "6"],
                ["3", "4", "7", "8"],
                ["9", "a", "d", "e"],
                ["b", "c", "f", "g"],
            ])
        )

    def test_should_draw_the_given_example(self):
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
        tile_1951_f_r000 = tiles_by_id[1951].flip()
        tile_2311_f_r000 = tiles_by_id[2311].flip()
        tile_3079_r_r000 = tiles_by_id[3079]
        tile_2729_f_r000 = tiles_by_id[2729].flip()
        tile_1427_f_r000 = tiles_by_id[1427].flip()
        _, _, tile_2473_f_r270 = tiles_by_id[2473].flip().rotate()
        tile_2971_f_r000 = tiles_by_id[2971].flip()
        tile_1489_f_r000 = tiles_by_id[1489].flip()
        _, tile_1171_f_r180, _ = tiles_by_id[1171].flip().rotate()

        jigsaw = [
            [tile_1951_f_r000, tile_2311_f_r000, tile_3079_r_r000],
            [tile_2729_f_r000, tile_1427_f_r000, tile_2473_f_r270],
            [tile_2971_f_r000, tile_1489_f_r000, tile_1171_f_r180]
        ]

        # WHEN
        drawing = _draw_picture(jigsaw)

        # THEN
        assert_that(
            "\n".join((
                "".join(row)
                for row in drawing
            )),
            equal_to(""".#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###""")
        )


class TestPattern:
    def test_should_parse_a_pattern(self):
        # GIVEN
        raw = [
            "                  #",
            "#    ##    ##    ###",
            " #  #  #  #  #  #"
        ]

        # WHEN
        pattern = Pattern.parse(raw)

        # THEN
        assert_that(
            pattern.shape,
            equal_to([
                [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "#"],
                ["#", None, None, None, None, "#", "#", None, None, None, None, "#", "#", None, None, None, None, "#", "#", "#"],
                [None, "#", None, None, "#", None, None, "#", None, None, "#", None, None, "#", None, None, "#"]
            ])
        )

    def test_should_count_the_number_of_pattern(self):
        # GIVEN
        drawing = list(map(
            list,
            [
                ".####...#####..#...###..",
                "#####..#..#.#.####..#.#.",
                ".#.#...#.###...#.##.##..",
                "#.#.##.###.#.##.##.#####",
                "..##.###.####..#.####.##",
                "...#.#..##.##...#..#..##",
                "#.##.#..#.#..#..##.#.#..",
                ".###.##.....#...###.#...",
                "#.####.#.#....##.#..#.#.",
                "##...#..#....#..#...####",
                "..#.##...###..#.#####..#",
                "....#.##.#.#####....#...",
                "..##.##.###.....#.##..#.",
                "#...#...###..####....##.",
                ".#.##...#.##.#.#.###...#",
                "#.###.#..####...##..#...",
                "#.###...#.##...#.######.",
                ".###.###.#######..#####.",
                "..##.#..#..#.#######.###",
                "#.#..##.########..#..##.",
                "#.#####..#.#...##..#....",
                "#....##..#.#########..##",
                "#...#.....#..##...###.##",
                "#..###....##.#...##.##.#",
            ]
        ))
        pattern = Pattern.parse([
            "                  #",
            "#    ##    ##    ###",
            " #  #  #  #  #  #"
        ])

        # WHEN
        occurrences = pattern.count_occurrences(drawing)

        # THEN
        assert_that(
            occurrences,
            equal_to(2)
        )


class TestGetNextCoordinates:
    def test_should_return_next_coordinates_in_middle(self):
        # GIVEN
        jigsaw_size = 5
        coordinates = (2, 3)

        # WHEN
        next_coord = _get_next_coordinates(jigsaw_size, coordinates)

        # THEN
        assert_that(next_coord, equal_to((2, 4)))

    def test_should_return_next_coordinates_at_end_of_row(self):
        # GIVEN
        jigsaw_size = 5
        coordinates = (2, 4)

        # WHEN
        next_coord = _get_next_coordinates(jigsaw_size, coordinates)

        # THEN
        assert_that(next_coord, equal_to((3, 0)))

    def test_should_return_none_at_end_of_jigsaw(self):
        # GIVEN
        jigsaw_size = 5
        coordinates = (4, 4)

        # WHEN
        next_coord = _get_next_coordinates(jigsaw_size, coordinates)

        # THEN
        assert_that(next_coord, equal_to(None))


class TestDoJigsaw:
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
        tiles_by_id = {
            tile.id: tile
            for tile in _parse(raw_tiles.splitlines(keepends=True))
        }
        corners = _find_corners(tiles_by_id)

        # WHEN
        jigsaw = _do_jigsaw(
            tiles_by_id,
            corners
        )

        # THEN
        assert_that(jigsaw is None, equal_to(False))

        jigsaw_ids = [
            [tile.id for tile in row]
            for row in jigsaw
        ]
        reference = [
            [1951, 2311, 3079],
            [2729, 1427, 2473],
            [2971, 1489, 1171]
        ]
        # noinspection PyTypeChecker
        assert_that(
            jigsaw_ids,
            # The result is the reference in any order, meaning we don't know
            # which corner will be use in top left.
            # So the result has to be one of the height possibility with rotations and flips
            any_of(
                equal_to(reference),
                equal_to(_rotate_mut(deepcopy(reference))),
                equal_to(_rotate_mut(_rotate_mut(deepcopy(reference)))),
                equal_to(_rotate_mut(_rotate_mut(_rotate_mut(deepcopy(reference))))),
                equal_to(_flip_mut(reference)),
                equal_to(_rotate_mut(deepcopy(_flip_mut(reference)))),
                equal_to(_rotate_mut(_rotate_mut(deepcopy(_flip_mut(reference))))),
                equal_to(_rotate_mut(_rotate_mut(_rotate_mut(deepcopy(_flip_mut(reference))))))
            )
        )


class TestCanUseTitle:
    def test_should_do_the_given_jigsaw_tile_by_tile(self):
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
        in_progress_jigsaw = _generate_empty_jigsaw(3)
        tile_1951_f_r000 = tiles_by_id[1951].flip()
        in_progress_jigsaw[0][0] = tile_1951_f_r000

        # WHEN placing 2311
        tile_2311_f_r000 = tiles_by_id[2311].flip()
        can_use_2311 = _can_use_tile(
            in_progress_jigsaw,
            tile_2311_f_r000,
            (0, 1)
        )
        # THEN should be able to use 2311
        assert_that(can_use_2311, equal_to(True))

        # WHEN placing 3079
        in_progress_jigsaw[0][1] = tile_2311_f_r000
        tile_3079_r_r000 = tiles_by_id[3079]
        can_use_3079 = _can_use_tile(
            in_progress_jigsaw,
            tile_3079_r_r000,
            (0, 2)
        )
        # THEN should be able to use 3079
        assert_that(can_use_3079, equal_to(True))

        in_progress_jigsaw[0][2] = tile_3079_r_r000
        # WHEN placing 2729
        tile_2729_f_r000 = tiles_by_id[2729].flip()
        can_use_2729 = _can_use_tile(
            in_progress_jigsaw,
            tile_2729_f_r000,
            (1, 0)
        )
        # THEN should be able to use 2729
        assert_that(can_use_2729, equal_to(True))

        in_progress_jigsaw[1][0] = tile_2729_f_r000
        # WHEN placing 1427
        tile_1427_f_r000 = tiles_by_id[1427].flip()
        can_use_1427 = _can_use_tile(
            in_progress_jigsaw,
            tile_1427_f_r000,
            (1, 1)
        )
        # THEN should be able to use 1427
        assert_that(can_use_1427, equal_to(True))

        in_progress_jigsaw[1][1] = tile_1427_f_r000
        # WHEN placing 2473
        _, _, tile_2473_f_r270 = tiles_by_id[2473].flip().rotate()
        can_use_2473 = _can_use_tile(
            in_progress_jigsaw,
            tile_2473_f_r270,
            (1, 2)
        )
        # THEN should be able to use 2473
        assert_that(can_use_2473, equal_to(True))

        in_progress_jigsaw[1][2] = tile_2473_f_r270
        # WHEN placing 2971
        tile_2971_f_r000 = tiles_by_id[2971].flip()
        can_use_2971 = _can_use_tile(
            in_progress_jigsaw,
            tile_2971_f_r000,
            (2, 0)
        )
        # THEN should be able to use 2971
        assert_that(can_use_2971, equal_to(True))

        in_progress_jigsaw[2][0] = tile_2971_f_r000
        # WHEN placing 1489
        tile_1489_f_r000 = tiles_by_id[1489].flip()
        can_use_1489 = _can_use_tile(
            in_progress_jigsaw,
            tile_1489_f_r000,
            (2, 1)
        )
        # THEN should be able to use 1489
        assert_that(can_use_1489, equal_to(True))

        in_progress_jigsaw[2][1] = tile_1489_f_r000
        # WHEN placing 1171
        _, tile_1171_f_r180, _ = tiles_by_id[1171].flip().rotate()
        can_use_1171 = _can_use_tile(
            in_progress_jigsaw,
            tile_1171_f_r180,
            (2, 2)
        )
        # THEN should be able to use 1171
        assert_that(can_use_1171, equal_to(True))


class TestSolvePart2:
    def test_should_solve_the_given_example(self):
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
        start = time.time()
        res = solve_part2(
            _parse(raw_tiles.splitlines(keepends=True))
        )
        end = time.time()
        print(f"solution computed in {(end - start) * 1000}ms")

        # THEN
        assert_that(res, equal_to(273))
