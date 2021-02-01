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

--- Part Two ---

The tile floor in the lobby is meant to be a living art exhibit. Every day, the tiles are all flipped according to the
following rules:
    Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
Here, tiles immediately adjacent means the six tiles directly touching the tile in question.
The rules are applied simultaneously to every tile; put another way, it is first determined which tiles need to be
flipped, then they are all flipped at the same time.
In the above example, the number of black tiles that are facing up after the given number of days has passed is as
follows:

Day 1: 15
Day 2: 12
Day 3: 25
Day 4: 14
Day 5: 23
Day 6: 28
Day 7: 41
Day 8: 37
Day 9: 49
Day 10: 37

Day 20: 132
Day 30: 259
Day 40: 406
Day 50: 566
Day 60: 788
Day 70: 1106
Day 80: 1373
Day 90: 1844
Day 100: 2208

After executing this process a total of 100 times, there would be 2208 black tiles facing up.
How many tiles will be black after 100 days?

"""
import os
import time
from collections import defaultdict
from collections.abc import Iterator, Iterable
from enum import Enum
from functools import reduce
from typing import DefaultDict, NamedTuple, Dict

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


def _flip_tile(directions: Iterable[Direction],
               tiles: DefaultDict[Coordinate, bool],
               from_tile: Coordinate = Coordinate(x=0, y=0)):
    coord = from_tile.move_multiple(directions)
    tiles[coord] = not tiles[coord]


def solve_part1(tiles_to_flip: Iterable[Iterable[Direction]]):
    tiles: DefaultDict[Coordinate, bool] = defaultdict(lambda: False)
    for directions in tiles_to_flip:
        _flip_tile(directions, tiles)

    return _count_black(tiles), tiles


def _count_black(tiles: Dict[Coordinate, bool]) -> int:
    return sum(filter(True.__eq__, tiles.values()))


def _get_neighbors(coord: Coordinate, include_self: bool = False) -> Iterator[Coordinate]:
    if include_self:
        yield coord
    for direction in Direction:
        yield coord.move(direction)


def _count_neighbors_black(coord: Coordinate,
                           tiles: Dict[Coordinate, bool]) -> int:
    return sum((
        True
        for neighbor in _get_neighbors(coord)
        if tiles.get(neighbor)
    ))


def _get_black_tiles(tiles: Dict[Coordinate, bool]) -> Iterable[Coordinate]:
    return (
        coord
        for coord, black in tiles.items()
        if black
    )


def _should_be_black(tile: Coordinate,
                     tiles: Dict[Coordinate, bool]) -> bool:
    # Any black tile with zero or more than 2 black tiles immediately
    # adjacent to it is flipped to white.
    # Any white tile with exactly 2 black tiles immediately adjacent
    # to it is flipped to black.
    black_neighbors = _count_neighbors_black(tile, tiles)
    if tiles.get(tile):
        # the tile is already black, so it will stay black if 1 or 2 neighbors are black
        return 0 < black_neighbors < 3

    # the tile is white, we want exactly 2 black neighbors
    return black_neighbors == 2


def _do_daily_flips(tiles: Dict[Coordinate, bool]) -> Dict[Coordinate, bool]:
    # we get all the black tiles and we analyze the neighbors
    return {
        tile: True
        for black_tile in _get_black_tiles(tiles)
        for tile in _get_neighbors(black_tile, include_self=True)
        if _should_be_black(tile, tiles)
    }


def do_x_daily_flips(tiles: Dict[Coordinate, bool], number_of_days: int) -> Dict[Coordinate, bool]:
    return reduce(
        lambda acc, _: _do_daily_flips(acc),
        range(number_of_days),
        tiles
    )


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _list_of_directions = _parse(file.readlines())

        start = time.time()
        solution_part1, _tiles = solve_part1(_list_of_directions)
        end = time.time()
        print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        assert solution_part1 == 277

        start = time.time()
        _tiles_after_day100 = do_x_daily_flips(_tiles, number_of_days=100)
        solution_part2 = _count_black(_tiles_after_day100)
        end = time.time()
        print(f"solution (part2): {solution_part2} in {(end - start) * 1000}ms")
        assert solution_part2 == 3531
