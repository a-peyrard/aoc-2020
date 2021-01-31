"""
-- Day 24: Lobby Layout ---

Your raft makes it to the tropical island; it turns out that the small crab was an excellent navigator. You make your
way to the resort.
As you enter the lobby, you discover a small problem: the floor is being renovated. You can't even reach the check-in
desk until they've finished installing the new tile floor.
The tiles are all hexagonal; they need to be arranged in a hex grid with a very specific color pattern. Not in the mood
to wait, you offer to help figure out the pattern.
The tiles are all white on one side and black on the other. They start with the white side facing up. The lobby is large
 enough to fit whatever pattern might need to appear there.
A member of the renovation crew gives you a list of the tiles that need to be flipped over (your puzzle input). Each
line in the list identifies a single tile that needs to be flipped by giving a series of steps starting from a reference
 tile in the very center of the room. (Every line starts from the same reference tile.)
Because the tiles are hexagonal, every tile has six neighbors: east, southeast, southwest, west, northwest, and
northeast. These directions are given in your list, respectively, as e, se, sw, w, nw, and ne. A tile is identified by
a series of these directions with no delimiters; for example, esenee identifies the tile you land on if you start at
the reference tile and then move one tile east, one tile southeast, one tile northeast, and one tile east.
Each time a tile is identified, it flips from white to black or from black to white. Tiles might be flipped more than
once. For example, a line like esew flips a tile immediately adjacent to the reference tile, and a line like nwwswee
flips the reference tile itself.
Here is a larger example:

sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew

In the above example, 10 tiles are flipped once (to black), and 5 more are flipped twice (to black, then back to white).
 After all of these instructions have been followed, a total of 10 tiles are black.
Go through the renovation crew's list and determine which tiles they need to flip. After all of the instructions have
been followed, how many tiles are left with the black side up?

"""
import os
import time
from collections import defaultdict
from collections.abc import Iterator, Iterable
from enum import Enum
from functools import reduce
from typing import DefaultDict, NamedTuple

from aoc.util.list import count

DEBUG = False


class Direction(Enum):
    NE = "ne"
    E = "e"
    SE = "se"
    SW = "sw"
    W = "w"
    NW = "nw"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Coordinate(NamedTuple):
    x: int
    y: int

    def move(self, direction: Direction) -> 'Coordinate':
        if direction == Direction.NE:
            return Coordinate(self.x + 1, self.y - 1)
        if direction == Direction.E:
            return Coordinate(self.x + 1, self.y)
        if direction == Direction.SE:
            return Coordinate(self.x, self.y + 1)
        if direction == Direction.SW:
            return Coordinate(self.x - 1, self.y + 1)
        if direction == Direction.W:
            return Coordinate(self.x - 1, self.y)
        if direction == Direction.NW:
            return Coordinate(self.x, self.y - 1)

    def move_multiple(self, directions: Iterable[Direction]) -> 'Coordinate':
        return reduce(
            lambda coord, direction: coord.move(direction),
            directions,
            self
        )


def _parse(lines: Iterable[str]) -> Iterable[Iterable[Direction]]:
    return map(_parse_directions, lines)


def _parse_directions(line: str) -> Iterator[Direction]:
    safe_line = line.strip()
    index = 0
    while index < len(safe_line):
        if index + 1 < len(safe_line):
            two_chars = safe_line[index:index + 2]
            if Direction.has_value(two_chars):
                yield Direction(two_chars)
                index += 2
                continue

        yield Direction(safe_line[index])
        index += 1


def _flip_tile(tiles: DefaultDict[Coordinate, bool],
               directions: Iterable[Direction],
               from_tile: Coordinate = Coordinate(x=0, y=0)):
    coord = from_tile.move_multiple(directions)
    tiles[coord] = not tiles[coord]


def solve_part1(tiles_to_flip: Iterable[Iterable[Direction]]):
    tiles: DefaultDict[Coordinate, bool] = defaultdict(lambda: False)
    for directions in tiles_to_flip:
        _flip_tile(tiles, directions)

    return count(filter(True.__eq__, tiles.values()))


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _list_of_directions = _parse(file.readlines())

        start = time.time()
        solution_part1 = solve_part1(_list_of_directions)
        end = time.time()
        print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        assert solution_part1 == 277
