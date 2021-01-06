"""
--- Day 17: Conway Cubes ---

As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the North Pole contact
you. They'd like some help debugging a malfunctioning experimental energy source aboard one of their super-secret
imaging satellites.
The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained in a pocket
dimension! When you hear it's having problems, you can't help but agree to take a look.
The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional coordinate (x,y,z), there
exists a single cube which is either active or inactive.
In the initial state of the pocket dimension, almost all cubes start inactive. The only exception to this is a small
flat region of cubes (your puzzle input); the cubes in this region start in the specified active (#) or inactive (.)
state.
The energy source then proceeds to boot up by executing six cycles.
Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most
1. For example, given the cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3,
and so on.
During a cycle, all cubes simultaneously change their state according to the following rules:
    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the
    cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube
    remains inactive.
The engineers responsible for this experimental energy source would like you to simulate the pocket dimension and
determine what the configuration of cubes should be at the end of the six-cycle boot process.
For example, consider the following initial state:
.#.
..#
###
Even though the pocket dimension is 3-dimensional, this initial state represents a small 2-dimensional slice of it.
(In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)
Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle
is shown layer-by-layer at each given z coordinate (and the frame of view follows the active cells in each cycle):

Before any cycles:

z=0
.#.
..#
###

After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.

After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....

After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......

After the full six-cycle boot process completes, 112 cubes are left in the active state.
Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after
the sixth cycle?

"""
import os
import time
from copy import deepcopy
from typing import List, Tuple

PocketDimension = List[List[List[bool]]]
Coordinate = Tuple[int, int, int]


def count_active(pocket: PocketDimension) -> int:
    return sum((
        sum((
            sum(line)
            for line in z_layer
        ))
        for z_layer in pocket
    ))


def _count_active_neighbors(coord: Coordinate, pocket: PocketDimension) -> int:
    x, y, z = coord
    counter = 0
    for z_idx in range(z - 1, z + 2):
        for y_idx in range(y - 1, y + 2):
            for x_idx in range(x - 1, x + 2):
                if z_idx != z or y_idx != y or x_idx != x:
                    if pocket[z_idx][y_idx][x_idx]:
                        counter += 1

    return counter


def execute_cycle(cycle_idx: int, cycles: int, pocket: PocketDimension) -> PocketDimension:
    margin = cycles - cycle_idx
    result = _init_empty_pocket(pocket)
    for z in range(margin, len(pocket) - margin):
        for y in range(margin, len(pocket[z]) - margin):
            for x in range(margin, len(pocket[z][y]) - margin):
                actives = _count_active_neighbors((x, y, z), pocket)
                if pocket[z][y][x]:
                    result[z][y][x] = actives in (2, 3)
                else:
                    result[z][y][x] = actives == 3

    return result


def _init_empty_pocket(pocket: PocketDimension) -> PocketDimension:
    return [
        [
            [False] * len(pocket[z][y])
            for y in range(len(pocket[z]))
        ]
        for z in range(len(pocket))
    ]


def solve_part1(lines: List[str], cycles: int) -> int:
    pocket = _parse(lines, cycles)
    for cycle_idx in range(cycles):
        pocket = execute_cycle(cycle_idx, cycles, pocket)

    return count_active(pocket)


def _parse(lines: List[str], cycles: int) -> PocketDimension:
    growth = 2 * (cycles + 1)
    x_size = len(lines[0].rstrip()) + growth
    y_size = len(lines) + growth

    # parse the flat region
    initial_flat_region = list(
        map(
            lambda l: list(map("#".__eq__, l.rstrip())),
            lines
        )
    )

    # put the flat region into the big cube that we will need for X cycles
    half_growth = growth // 2
    empty_layer = [[False] * x_size for _ in range(y_size)]
    pocket = []
    # add some empty z-layers
    for _ in range(half_growth):
        pocket.append(deepcopy(empty_layer))

    # add our initial flat region surrounded by inactive cubes
    extended_initial_region = []
    for _ in range(half_growth):
        extended_initial_region.append([False] * x_size)

    for line in initial_flat_region:
        for _ in range(half_growth):
            line.insert(0, False)
            line.append(False)
        extended_initial_region.append(line)

    for _ in range(half_growth):
        extended_initial_region.append([False] * x_size)

    pocket.append(extended_initial_region)

    # add some empty z-layers
    for _ in range(half_growth):
        pocket.append(deepcopy(empty_layer))

    return pocket


def _print_pocket_dimension(pocket: PocketDimension):
    # print z-layers side by side
    for row_idx in range(len(pocket[0])):
        line = ""
        for z_layer in pocket:
            line += "".join(map(
                lambda cube: "#" if cube else ".",
                z_layer[row_idx]
            )) + " "
        print(line)


def _transform_pocket_to_ints(pocket: PocketDimension) -> List[List[List[int]]]:
    """
    For debugging purposes, as this is easier to read matrix of 0/1 than matrix of True/False
    """
    return [
        [
            [
                1 if cube else 0
                for cube in line
            ]
            for line in z_layer
        ]
        for z_layer in pocket
    ]


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _lines = list(file.readlines())

        start = time.time()
        solution_part1 = solve_part1(_lines, 6)
        end = time.time()
        print(f"solution (part1): {solution_part1} in {(end - start) * 1000}ms")
        assert solution_part1 == 230
