"""
--- Day 20: Jurassic Jigsaw ---

The high-speed train leaves the forest and quickly carries you south. You can even see a desert in the distance! Since
you have some spare time, you might as well see if there was anything interesting in the image the Mythical Information
Bureau satellite captured.
After decoding the satellite messages, you discover that the data actually contains many small images created by the
satellite's camera array. The camera array consists of many cameras; rather than produce a single square image, they
produce many smaller square image tiles that need to be reassembled back into a single image.
Each camera in the camera array returns a single monochrome image tile with a random unique ID number. The tiles (your
puzzle input) arrived in a random order.
Worse yet, the camera array appears to be malfunctioning: each image tile has been rotated and flipped to a random
orientation. Your first task is to reassemble the original image by orienting the tiles so they fit together.
To show how the tiles should be reassembled, each tile's image data includes a border that should line up exactly with
its adjacent tiles. All tiles have this border, and the border lines up exactly when the tiles are both oriented
correctly. Tiles at the edge of the image also have this border, but the outermost edges won't line up with any other
tiles.
For example, suppose you have the following nine tiles:

Tile 2311:
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
..#.###...

By rotating, flipping, and rearranging them, you can find a square arrangement that causes all adjacent borders to line
up:

#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##.....

For reference, the IDs of the above tiles are:
1951    2311    3079
2729    1427    2473
2971    1489    1171
To check that you've assembled the image correctly, multiply the IDs of the four corner tiles together. If you do this
with the assembled tiles from the example above, you get 1951 * 3079 * 2971 * 1171 = 20899048083289.
Assemble the tiles into an image. What do you get if you multiply together the IDs of the four corner tiles?

"""
import os
import re
from enum import Enum
from typing import List, Tuple, Iterable, NamedTuple

from aoc.util.text import generate_paragraphs


class Direction(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


class Tile(NamedTuple):
    id: int
    top: int
    right: int
    bottom: int
    left: int

    def match(self, other: 'Tile') -> Direction:
        if self.top == other.bottom:
            return Direction.TOP
        if self.right == other.left:
            return Direction.RIGHT
        if self.bottom == other.top:
            return Direction.BOTTOM
        if self.left == other.right:
            return Direction.LEFT

    def rotate(self) -> Tuple['Tile', 'Tile', 'Tile']:
        rotation_90 = self._rotate_90()
        rotation_180 = rotation_90._rotate_90()
        rotation_270 = rotation_180._rotate_90()
        return (
            rotation_90,
            rotation_180,
            rotation_270
        )

    def _rotate_90(self) -> 'Tile':
        pass  # fixme

    def flip(self) -> Tuple['Tile', 'Tile', 'Tile']:
        flip_x = self._flip_x()
        flip_y = self._flip_y()
        flip_xy = flip_x._flip_y()
        return (
            flip_x,
            flip_y,
            flip_xy
        )

    def _flip_x(self) -> 'Tile':
        pass  # fixme

    def _flip_y(self) -> 'Tile':
        pass  # fixme


TILE_REGEX = re.compile(r"Tile (\d+):")


def _parse(lines: List[str]) -> List[Tile]:
    return [
        _parse_tile(raw_tile)
        for raw_tile in generate_paragraphs(lines)
    ]


def _parse_tile(lines: List[str]) -> Tile:
    # Tile 2311:
    # ..##.#..#.
    # ##..#.....
    # #...##..#.
    # ####.#...#
    # ##.##.###.
    # ##...#.###
    # .#.#.#..##
    # ..#....#..
    # ###...#.#.
    # ..###..###
    id_line, *tile_lines = lines
    tile_id = _parse_tile_id(id_line)
    top = _parse_to_binary(tile_lines[0])
    right = _parse_to_binary([
        line[9]
        for line in tile_lines
    ])
    bottom = _parse_to_binary(tile_lines[9])
    left = _parse_to_binary([
        line[0]
        for line in tile_lines
    ])
    return Tile(
        id=tile_id,
        top=top,
        right=right,
        bottom=bottom,
        left=left
    )


def _parse_tile_id(line: str) -> int:
    id_matcher = TILE_REGEX.search(line)
    if not id_matcher or len(id_matcher.groups()) != 1:
        raise ValueError(f"Unable to extract tile id from {line}")

    return int(id_matcher.group(1))


def _parse_to_binary(values: Iterable[str]) -> int:
    return int("".join(map(lambda c: "1" if c == "#" else "0", values)), 2)


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        pass
        # _rules, _messages = _parse(list(file.readlines()))
        #
        # start = time.time()
        # solution_part1 = solve_part1(_messages, _rules, rule_idx=0)
        # end = time.time()
        # print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        # assert solution_part1 == 102
        #
        # start = time.time()
        # solution_part2 = solve_part2(_messages, _rules, rule_idx=0)
        # end = time.time()
        # print(f"solution (part2): {solution_part2} in {(end - start) * 1000}ms")
        # assert solution_part2 == 318
