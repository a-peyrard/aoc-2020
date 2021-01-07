"""
--- Part Two ---

For some reason, your simulated results don't match what the experimental energy source engineers expected. Apparently,
the pocket dimension actually has four spatial dimensions, not three.
The pocket dimension contains an infinite 4-dimensional grid. At every integer 4-dimensional coordinate (x,y,z,w), there
 exists a single cube (really, a hypercube) which is still either active or inactive.
Each cube only ever considers its neighbors: any of the 80 other cubes where any of their coordinates differ by at most
1. For example, given the cube at x=1,y=2,z=3,w=4, its neighbors include the cube at x=2,y=2,z=3,w=3, the cube at
x=0,y=2,z=3,w=4, and so on.
The initial state of the pocket dimension still consists of a small flat region of cubes. Furthermore, the same rules
for cycle updating still apply: during each cycle, consider the number of active neighbors of each cube.
For example, consider the same initial state as in the example above. Even though the pocket dimension is 4-dimensional,
 this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1x1
 region of the 4-dimensional space.)
Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is
 shown layer-by-layer at each given z and w coordinate:
Before any cycles:

z=0, w=0
.#.
..#
###


After 1 cycle:

z=-1, w=-1
#..
..#
.#.

z=0, w=-1
#..
..#
.#.

z=1, w=-1
#..
..#
.#.

z=-1, w=0
#..
..#
.#.

z=0, w=0
#.#
.##
.#.

z=1, w=0
#..
..#
.#.

z=-1, w=1
#..
..#
.#.

z=0, w=1
#..
..#
.#.

z=1, w=1
#..
..#
.#.


After 2 cycles:

z=-2, w=-2
.....
.....
..#..
.....
.....

z=-1, w=-2
.....
.....
.....
.....
.....

z=0, w=-2
###..
##.##
#...#
.#..#
.###.

z=1, w=-2
.....
.....
.....
.....
.....

z=2, w=-2
.....
.....
..#..
.....
.....

z=-2, w=-1
.....
.....
.....
.....
.....

z=-1, w=-1
.....
.....
.....
.....
.....

z=0, w=-1
.....
.....
.....
.....
.....

z=1, w=-1
.....
.....
.....
.....
.....

z=2, w=-1
.....
.....
.....
.....
.....

z=-2, w=0
###..
##.##
#...#
.#..#
.###.

z=-1, w=0
.....
.....
.....
.....
.....

z=0, w=0
.....
.....
.....
.....
.....

z=1, w=0
.....
.....
.....
.....
.....

z=2, w=0
###..
##.##
#...#
.#..#
.###.

z=-2, w=1
.....
.....
.....
.....
.....

z=-1, w=1
.....
.....
.....
.....
.....

z=0, w=1
.....
.....
.....
.....
.....

z=1, w=1
.....
.....
.....
.....
.....

z=2, w=1
.....
.....
.....
.....
.....

z=-2, w=2
.....
.....
..#..
.....
.....

z=-1, w=2
.....
.....
.....
.....
.....

z=0, w=2
###..
##.##
#...#
.#..#
.###.

z=1, w=2
.....
.....
.....
.....
.....

z=2, w=2
.....
.....
..#..
.....
.....

After the full six-cycle boot process completes, 848 cubes are left in the active state.
Starting with your given initial configuration, simulate six cycles in a 4-dimensional space. How many cubes are left in
 the active state after the sixth cycle?

"""
import os
import time
from copy import deepcopy
from typing import List, Tuple

PocketDimension = List[List[List[List[bool]]]]
Coordinate = Tuple[int, int, int, int]


def count_active(pocket: PocketDimension) -> int:
    return sum((
        sum((
            sum((
                sum(line)
                for line in z_layer
            ))
            for z_layer in w_layer
        ))
        for w_layer in pocket
    ))


def _count_active_neighbors(coord: Coordinate, pocket: PocketDimension) -> int:
    x, y, z, w = coord
    counter = 0
    for w_idx in range(w - 1, w + 2):
        for z_idx in range(z - 1, z + 2):
            for y_idx in range(y - 1, y + 2):
                for x_idx in range(x - 1, x + 2):
                    if w_idx != w or z_idx != z or y_idx != y or x_idx != x:
                        if pocket[w_idx][z_idx][y_idx][x_idx]:
                            counter += 1

    return counter


def execute_cycle(cycle_idx: int, cycles: int, pocket: PocketDimension) -> PocketDimension:
    margin = cycles - cycle_idx
    result = _init_empty_pocket(pocket)
    for w in range(margin, len(pocket) - margin):
        for z in range(margin, len(pocket[w]) - margin):
            for y in range(margin, len(pocket[w][z]) - margin):
                for x in range(margin, len(pocket[w][z][y]) - margin):
                    actives = _count_active_neighbors((x, y, z, w), pocket)
                    if pocket[w][z][y][x]:
                        result[w][z][y][x] = actives in (2, 3)
                    else:
                        result[w][z][y][x] = actives == 3

    return result


def _init_empty_pocket(pocket: PocketDimension) -> PocketDimension:
    return [
        [
            [
                [False] * len(pocket[w][z][y])
                for y in range(len(pocket[w][z]))
            ]
            for z in range(len(pocket[w]))
        ]
        for w in range(len(pocket))
    ]


def _init_empty_three_dimensions_pocket(x_size: int,
                                        y_size: int,
                                        z_size: int) -> List[List[List[int]]]:
    return [
        [
            [False] * x_size
            for _ in range(y_size)
        ]
        for _ in range(z_size)
    ]


# noinspection DuplicatedCode
def solve_part2(lines: List[str], cycles: int) -> int:
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

    # add some empty w-layers
    for _ in range(half_growth):
        pocket.append(_init_empty_three_dimensions_pocket(
            x_size=x_size,
            y_size=y_size,
            z_size=1 + growth
        ))

    main_w_layer = []
    # add some empty z-layers
    for _ in range(half_growth):
        main_w_layer.append(deepcopy(empty_layer))

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

    main_w_layer.append(extended_initial_region)

    # add some empty z-layers
    for _ in range(half_growth):
        main_w_layer.append(deepcopy(empty_layer))

    pocket.append(main_w_layer)

    # add some empty w-layers
    for _ in range(half_growth):
        pocket.append(_init_empty_three_dimensions_pocket(
            x_size=x_size,
            y_size=y_size,
            z_size=1 + growth
        ))

    return pocket


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "input")) as file:
        _lines = list(file.readlines())

        start = time.time()
        solution_part2 = solve_part2(_lines, 6)
        end = time.time()
        print(f"solution (part2): {solution_part2} in {(end - start) * 1000}ms")
        assert solution_part2 == 1600
