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

--- Part Two ---

Now, you're ready to check the image for sea monsters.
The borders of each tile are not part of the actual image; start by removing them.
In the example above, the tiles become:

.#.#..#. ##...#.# #..#####
###....# .#....#. .#......
##.##.## #.#.#..# #####...
###.#### #...#.## ###.#..#
##.#.... #.##.### #...#.##
...##### ###.#... .#####.#
....#..# ...##..# .#.###..
.####... #..#.... .#......

#..#.##. .#..###. #.##....
#.####.. #.####.# .#.###..
###.#.#. ..#.#### ##.#..##
#.####.. ..##..## ######.#
##..##.# ...#...# .#.#.#..
...#..#. .#.#.##. .###.###
.#.#.... #.##.#.. .###.##.
###.#... #..#.##. ######..

.#.#.### .##.##.# ..#.##..
.####.## #.#...## #.#..#.#
..#.#..# ..#.#.#. ####.###
#..####. ..#.#.#. ###.###.
#####..# ####...# ##....##
#.##..#. .#...#.. ####...#
.#.###.. ##..##.. ####.##.
...###.. .##...#. ..#..###

Remove the gaps to form the actual image:

.#.#..#.##...#.##..#####
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
...###...##...#...#..###

Now, you're ready to search for sea monsters! Because your image is monochrome, a sea monster will look like this:

                  #
#    ##    ##    ###
 #  #  #  #  #  #

When looking for this pattern in the image, the spaces can be anything; only the # need to match. Also, you might need
to rotate or flip your image before it's oriented correctly to find sea monsters. In the above image, after flipping and
 rotating it to the appropriate orientation, there are two sea monsters (marked with O):

.####...#####..#...###..
#####..#..#.#.####..#.#.
.#.#...#.###...#.##.O#..
#.O.##.OO#.#.OO.##.OOO##
..#O.#O#.O##O..O.#O##.##
...#.#..##.##...#..#..##
#.##.#..#.#..#..##.#.#..
.###.##.....#...###.#...
#.####.#.#....##.#..#.#.
##...#..#....#..#...####
..#.##...###..#.#####..#
....#.##.#.#####....#...
..##.##.###.....#.##..#.
#...#...###..####....##.
.#.##...#.##.#.#.###...#
#.###.#..####...##..#...
#.###...#.##...#.##O###.
.O##.#OO.###OO##..OOO##.
..O#.O..O..O.#O##O##.###
#.#..##.########..#..##.
#.#####..#.#...##..#....
#....##..#.#########..##
#...#.....#..##...###.##
#..###....##.#...##.##.#

Determine how rough the waters are in the sea monsters' habitat by counting the number of # that are not part of a sea
monster. In the above example, the habitat's water roughness is 273.
How many # are not part of a sea monster?

"""
import os
import re
import time
from enum import Enum
from math import prod, isqrt
from typing import List, Tuple, Iterable, NamedTuple, Set, Dict, TypeVar, Optional, Callable

from aoc.util.functional import compose
from aoc.util.list import flat_map
from aoc.util.matrix import initialize_matrix
from aoc.util.text import generate_paragraphs

DEBUG = False


T = TypeVar('T')


class Direction(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


class Tile(NamedTuple):
    @staticmethod
    def parse(lines: List[str]) -> 'Tile':
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

        inner_content = [
            list(tile_lines[line_idx][1:-1])
            for line_idx in range(1, 9)
        ]

        return Tile(
            id=tile_id,
            top=top,
            right=right,
            bottom=bottom,
            left=left,
            inner_content=inner_content
        )

    id: int
    top: int
    right: int
    bottom: int
    left: int
    inner_content: List[List[str]]
    flipped: bool = False
    rotation: int = 0

    def match(self, other: 'Tile') -> Iterable[Direction]:
        return (
            direction
            for direction in Direction
            if self.match_direction(other, direction)
        )

    def match_direction(self, other: 'Tile', direction: Direction) -> bool:
        if direction == Direction.TOP:
            return self.top == other.bottom
        if direction == Direction.RIGHT:
            return self.right == other.left
        if direction == Direction.BOTTOM:
            return self.bottom == other.top
        if direction == Direction.LEFT:
            return self.left == other.right
        raise ValueError(f"unexpected direction {direction}")

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
        return Tile(
            id=self.id,
            right=self.top,
            bottom=_reverse_binary(self.right, size=10),
            left=self.bottom,
            top=_reverse_binary(self.left, size=10),
            inner_content=self.inner_content,
            flipped=self.flipped,
            rotation=self.rotation + 90
        )

    def flip(self) -> 'Tile':
        return Tile(
            id=self.id,
            top=self.bottom,
            right=_reverse_binary(self.right, size=10),
            bottom=self.top,
            left=_reverse_binary(self.left, size=10),
            inner_content=self.inner_content,
            flipped=not self.flipped,
            rotation=self.rotation
        )

    def get_all_variants(self) -> List['Tile']:
        flipped = self.flip()
        tiles = [self, flipped]
        tiles.extend(self.rotate())
        tiles.extend(flipped.rotate())
        return tiles

    def draw(self):
        drawing = [
            row.copy()
            for row in self.inner_content
        ]
        mutations = []
        mutations.extend([_rotate_mut] * (self.rotation // 90))
        if self.flipped:
            mutations.append(_flip_mut)

        return compose(*mutations)(drawing)

    def __repr__(self) -> str:
        return f"tile_{self.id}_{'f' if self.flipped else 'r'}_r{self.rotation:03}"


class Pattern(NamedTuple):
    @staticmethod
    def parse(raw: List[str]):
        return Pattern(
            shape=list(map(Pattern._parse_row, raw))
        )

    @staticmethod
    def _parse_row(row: str) -> List[Optional[str]]:
        return [
            c if c.strip() else None
            for c in row
        ]

    shape: List[List[Optional[T]]]

    def count_occurrences(self, drawing: List[List[T]]) -> int:
        shape_height = len(self.shape)
        shape_width = max(map(len, self.shape))

        drawing_height = len(drawing)
        drawing_width = len(drawing[0])

        number_of_matches = 0
        row_idx = 0
        while row_idx < drawing_height - shape_height + 1:
            col_idx = 0
            while col_idx < drawing_width - shape_width + 1:
                match = all((
                    Pattern._match(piece, drawing[row_idx + shape_row_idx], col_idx)
                    for shape_row_idx, piece in enumerate(self.shape)
                ))
                if match:
                    number_of_matches += 1
                    col_idx += shape_width
                else:
                    col_idx += 1

            row_idx += 1

        return number_of_matches

    @staticmethod
    def _match(piece: List[T], line: List[T], offset: int) -> bool:
        for idx in range(0, len(piece)):
            item = piece[idx]
            if item and line[offset + idx] != item:
                return False

        return True


TILE_REGEX = re.compile(r"Tile (\d+):")


def _reverse_binary(num: int, size: int) -> int:
    res = 0
    for _ in range(size):
        res <<= 1
        if num & 1:
            res |= 1
        num >>= 1

    return res


def _parse(lines: Iterable[str]) -> List[Tile]:
    return [
        Tile.parse(raw_tile)
        for raw_tile in generate_paragraphs(lines)
    ]


def _parse_tile_id(line: str) -> int:
    id_matcher = TILE_REGEX.search(line)
    if not id_matcher or len(id_matcher.groups()) != 1:
        raise ValueError(f"Unable to extract tile id from {line}")

    return int(id_matcher.group(1))


def _parse_to_binary(values: Iterable[str]) -> int:
    return int("".join(map(lambda c: "1" if c == "#" else "0", values)), 2)


def _match_tile_against_peers(tile_id,
                              tiles_by_id: Dict[int, Tile]) -> List[Tuple[Tile, Direction, Tile]]:
    the_tile = tiles_by_id[tile_id]
    variants_to_match = [the_tile]
    remaining_tile_ids = set((
        tile.id
        for tid, tile in tiles_by_id.items()
        if tile_id != tid
    ))

    matches = _get_all_matches(variants_to_match, remaining_tile_ids, tiles_by_id)
    DEBUG and print(
        f"""
== for tile #{the_tile}
matches:
""" + "\n".join(map(str, matches))
    )
    return matches


def _get_all_matches(tiles: List[Tile],
                     available_tile_ids: Set[int],
                     tiles_by_id: Dict[int, Tile]) -> List[Tuple[Tile, Direction, Tile]]:

    matches: List[Tuple[Tile, Direction, Tile]] = []
    for tile in tiles:
        matches_for_tile = _get_all_matches_for_tile(tile, available_tile_ids, tiles_by_id)
        for direction, matching_tile in matches_for_tile:
            matches.append((tile, direction, matching_tile))

    return matches


def _get_all_matches_for_tile(tile: Tile,
                              available_tile_ids: Set[int],
                              tiles_by_id: Dict[int, Tile]) -> List[Tuple[Direction, Tile]]:

    possibles_matches = flat_map(map(
        lambda tile_id: tiles_by_id[tile_id].get_all_variants(),
        available_tile_ids
    ))
    return _get_all_matches_for_tile_from_list(
        tile,
        possibles_matches
    )


def _get_all_matches_for_tile_from_list(tile_to_match: Tile,
                                        tiles: List[Tile]) -> List[Tuple[Direction, Tile]]:
    matches: List[Tuple[Direction, Tile]] = []
    for tile in tiles:
        matching_directions = tile_to_match.match(tile)
        for matching_direction in matching_directions:
            matches.append((matching_direction, tile))

    False and DEBUG and print(f"\nfor tile {tile_to_match}, we have those matches:\n" + "\n".join(map(str, matches)))

    return matches


def _find_corners(tiles_by_id: Dict[int, Tile]) -> List[int]:
    corners = []
    for tile_id in tiles_by_id.keys():
        matches = _match_tile_against_peers(tile_id, tiles_by_id)
        if len(set((direction for _, direction, _ in matches))) == 2:
            corners.append(tile_id)

    DEBUG and print(f"\n\nPOSSIBLE CORNERS = {corners}")

    if len(corners) != 4:
        raise ValueError(f"Unable to find 4 corners, but {corners}")

    return corners


def solve_part1(tiles: List[Tile]) -> Tuple[int, List[int]]:
    tiles_by_id = {
        tile.id: tile
        for tile in tiles
    }

    corners = _find_corners(tiles_by_id)

    return prod(corners), corners


def _flip_mut(matrix: List[List[T]]) -> List[List[T]]:
    height = len(matrix)
    width = len(matrix[0])

    for row_idx in range(height // 2):
        target_row_idx = height - 1 - row_idx
        for col_idx in range(width):
            matrix[target_row_idx][col_idx], matrix[row_idx][col_idx] = \
                matrix[row_idx][col_idx], matrix[target_row_idx][col_idx]

    return matrix


def _rotate_mut(matrix: List[List[T]]) -> List[List[T]]:
    height = len(matrix)
    width = len(matrix[0])
    if height != width:
        raise ValueError(f"we need a square matrix in order to rotate (h: {height}, w: {width})")

    # 0 a 0 0 0
    # 0 0 0 0 b
    # 0 0 0 0 0
    # d 0 0 0 0
    # 0 0 0 c 0

    for inner_idx in range(height // 2):
        current_width = width - (2 * inner_idx)
        for idx in range(0, current_width - 1):
            # swap 4 cells in every pass of the loop
            a = matrix[inner_idx][inner_idx + idx]
            b = matrix[inner_idx + idx][inner_idx + current_width - 1]
            c = matrix[height - 1 - inner_idx][inner_idx + current_width - 1 - idx]
            d = matrix[height - 1 - inner_idx - idx][inner_idx]

            matrix[inner_idx + idx][inner_idx + current_width - 1], \
                matrix[height - 1 - inner_idx][inner_idx + current_width - 1 - idx], \
                matrix[height - 1 - inner_idx - idx][inner_idx], \
                matrix[inner_idx][inner_idx + idx] \
                = a, b, c, d

    return matrix


def _draw_picture(jigsaw: List[List[Tile]]) -> List[List[str]]:
    tile_drawing_size = len(jigsaw[0][0].inner_content)
    full_drawing_size = len(jigsaw) * tile_drawing_size
    result = initialize_matrix("", full_drawing_size)

    for row_idx, row in enumerate(jigsaw):
        for col_idx, tile in enumerate(row):
            tile_drawing = tile.draw()
            for tile_row_idx in range(tile_drawing_size):
                for tile_col_idx in range(tile_drawing_size):
                    result[
                        row_idx * tile_drawing_size + tile_row_idx
                    ][
                        col_idx * tile_drawing_size + tile_col_idx
                    ] = tile_drawing[tile_row_idx][tile_col_idx]

    return result


def _generate_empty_jigsaw(size: int) -> List[List[Optional[Tile]]]:
    row = [None] * size
    return [
        row.copy()
        for _ in range(size)
    ]


def _do_jigsaw(tiles_by_id: Dict[int, Tile],
               corners: List[int]) -> Optional[List[List[Tile]]]:
    # generate an empty jigsaw and place the first corner
    jigsaw_size = isqrt(len(tiles_by_id))
    in_progress_jigsaw = _generate_empty_jigsaw(jigsaw_size)
    # in_progress_jigsaw[0][0] = tiles_by_id[corners[0]]
    # used_tile_ids = {corners[0]}

    # now we need to launch the recursive analysis and try combinations to finish
    # the jigsaw, easy peasy 😅
    jigsaw = _do_jigsaw_rec(
        jigsaw_size,
        in_progress_jigsaw,
        set(),
        tiles_by_id,
        set(corners),
        coordinates=(0, 0)
    )

    return jigsaw


def _do_jigsaw_rec(jigsaw_size: int,
                   in_progress_jigsaw: List[List[Optional[Tile]]],
                   used_tile_ids: Set[int],
                   tiles_by_id: Dict[int, Tile],
                   corners: Set[int],
                   coordinates: Tuple[int, int]) -> Optional[List[List[Tile]]]:

    DEBUG and print(f"trying to find a tile for coordinate {coordinates}")

    if _is_corner(jigsaw_size, coordinates):
        # we need to place a corner
        possible_tiles = (
            tiles_by_id[tile_id]
            for tile_id in corners
            if tile_id not in used_tile_ids
        )
    else:
        # we need to place a tile that have not been used before and which is not a corner
        possible_tiles = (
            tiles_by_id[tile_id]
            for tile_id, tile in tiles_by_id.items()
            if tile_id not in used_tile_ids and tile_id not in corners
        )

    row, col = coordinates
    next_coord = _get_next_coordinates(jigsaw_size, coordinates)
    for possible_tile in possible_tiles:
        for variant in possible_tile.get_all_variants():
            DEBUG and print(f"...try {variant} for coord {coordinates}")
            if _can_use_tile(in_progress_jigsaw, variant, coordinates):
                DEBUG and print(f"🎉 we have a match for coord {coordinates}: {variant}")
                in_progress_jigsaw[row][col] = variant
                used_tile_ids.add(variant.id)
                if next_coord:
                    solution = _do_jigsaw_rec(
                        jigsaw_size,
                        in_progress_jigsaw,
                        used_tile_ids,
                        tiles_by_id,
                        corners,
                        next_coord
                    )
                    if solution:
                        return solution
                else:
                    return in_progress_jigsaw

                used_tile_ids.remove(variant.id)

    return None


def _is_corner(jigsaw_size: int,
               coordinates: Tuple[int, int]) -> bool:
    row, col = coordinates
    if row == 0:
        return col == 0 or col == jigsaw_size - 1
    if row == jigsaw_size - 1:
        return col == 0 or col == jigsaw_size - 1

    return False


def _can_use_tile(in_progress_jigsaw: List[List[Optional[Tile]]],
                  tile: Tile,
                  coordinates: Tuple[int, int]) -> bool:
    row, col = coordinates
    if col > 0:
        left_tile = in_progress_jigsaw[row][col - 1]
        if not left_tile.match_direction(tile, Direction.RIGHT):
            return False

    if row > 0:
        top_tile = in_progress_jigsaw[row - 1][col]
        if not top_tile.match_direction(tile, Direction.BOTTOM):
            return False

    return True


def _get_next_coordinates(jigsaw_size: int,
                          coordinates: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    row, col = coordinates
    if col < jigsaw_size - 1:
        return row, col + 1
    if row < jigsaw_size - 1:
        return row + 1, 0

    return None


def solve_part2(tiles: List[Tile],
                corners: Optional[List[int]] = None) -> int:
    tiles_by_id = {
        tile.id: tile
        for tile in tiles
    }

    corners = corners if corners else _find_corners(tiles_by_id)
    jigsaw = _do_jigsaw(tiles_by_id, corners)

    drawing = _draw_picture(jigsaw)
    pattern = Pattern.parse([
        "                  #",
        "#    ##    ##    ###",
        " #  #  #  #  #  #"
    ])

    transformations: List[Callable[[List[List[str]]], List[List[str]]]] = [
        lambda x: x,
        _rotate_mut,
        compose(_rotate_mut, _rotate_mut),
        compose(_rotate_mut, _rotate_mut, _rotate_mut),
        _flip_mut,
        _rotate_mut,
        compose(_rotate_mut, _rotate_mut),
        compose(_rotate_mut, _rotate_mut, _rotate_mut),
    ]
    number_of_monster = next(filter(
        lambda n: n > 0,
        (
            pattern.count_occurrences(transformation(drawing))
            for transformation in transformations
        )
    ))

    return _count_character(drawing, "#") - (15 * number_of_monster)


def _count_character(drawing: List[List[str]], character: str) -> int:
    return sum((
        sum(map(character.__eq__, row))
        for row in drawing
    ))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _tiles = _parse(file.readlines())

        start = time.time()
        solution_part1, _corners = solve_part1(_tiles)
        end = time.time()
        print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        assert solution_part1 == 19955159604613
