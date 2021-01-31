from hamcrest import contains_exactly, assert_that, equal_to, same_instance, not_none

from aoc.day24.lobby_layout import _parse_directions, Direction, _parse, Coordinate, solve_part1


class TestParseDirections:
    def test_should_parse_directions(self):
        # GIVEN
        raw = "wseweeenwnesenwwwswnew"

        # WHEN
        directions = _parse_directions(raw)

        # THEN
        assert_that(
            directions,
            contains_exactly(
                Direction.W,
                Direction.SE,
                Direction.W,
                Direction.E,
                Direction.E,
                Direction.E,
                Direction.NW,
                Direction.NE,
                Direction.SE,
                Direction.NW,
                Direction.W,
                Direction.W,
                Direction.SW,
                Direction.NE,
                Direction.W,
            )
        )


class TestParse:
    def test_should_parse_list_of_raw_directions(self):
        # GIVEN
        raw = """wsew
eee
nwne
senwww
swnew"""

        # WHEN
        res = _parse(raw.splitlines(keepends=True))

        # THEN
        assert_that(
            res,
            contains_exactly(
                contains_exactly(
                    Direction.W,
                    Direction.SE,
                    Direction.W
                ),
                contains_exactly(
                    Direction.E,
                    Direction.E,
                    Direction.E
                ),
                contains_exactly(
                    Direction.NW,
                    Direction.NE
                ),
                contains_exactly(
                    Direction.SE,
                    Direction.NW,
                    Direction.W,
                    Direction.W
                ),
                contains_exactly(
                    Direction.SW,
                    Direction.NE,
                    Direction.W
                )
            )
        )


class TestCoordinate:
    def test_should_move_to_another_direction(self):
        # GIVEN
        coord = Coordinate(x=0, y=0)

        # WHEN
        another_coord = coord.move(Direction.NW)

        # THEN
        assert_that(
            another_coord,
            equal_to(Coordinate(x=0, y=-1))
        )

    def test_should_move_and_go_back_to_initial_position(self):
        # GIVEN
        coord = Coordinate(x=0, y=0)

        # WHEN
        another_coord = coord.move(Direction.SW).move(Direction.NE)

        # THEN
        assert_that(another_coord, not_none())
        assert_that(another_coord, equal_to(coord))

    def test_should_jump_and_go_back_to_initial_tile_with_path(self):
        # GIVEN
        coord = Coordinate(x=0, y=0)

        # WHEN
        another_coord = coord.move_multiple((
            Direction.SE,
            Direction.SE,
            Direction.W,
            Direction.W,
            Direction.NW,
            Direction.NE,
            Direction.E,
        ))

        # THEN
        assert_that(another_coord, not_none())
        assert_that(another_coord, equal_to(coord))


class TestSolvePart1:
    def test_should_solve_given_example(self):
        # GIVEN
        raw = """sesenwnenenewseeswwswswwnenewsewsw
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
wseweeenwnesenwwwswnew"""

        # WHEN
        res = solve_part1(_parse(raw.splitlines(keepends=True)))

        # THEN
        assert_that(res, equal_to(10))
