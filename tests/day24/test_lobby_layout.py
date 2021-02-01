from hamcrest import contains_exactly, assert_that, equal_to, same_instance, not_none

from aoc.day24.lobby_layout import _parse_directions, Direction, _parse, Coordinate, solve_part1, do_x_daily_flips, \
    _count_black, move, move_multiple


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
        coord = complex(0, 0)

        # WHEN
        another_coord = move(coord, Direction.NW)

        # THEN
        assert_that(
            another_coord,
            equal_to(complex(0, -1))
        )

    def test_should_move_and_go_back_to_initial_position(self):
        # GIVEN
        coord = complex(0, 0)

        # WHEN
        another_coord = move(move(coord, Direction.SW), Direction.NE)

        # THEN
        assert_that(another_coord, equal_to(coord))

    def test_should_jump_and_go_back_to_initial_tile_with_path(self):
        # GIVEN
        coord = complex(0, 0)

        # WHEN
        another_coord = move_multiple(
            coord,
            (
                Direction.SE,
                Direction.SE,
                Direction.W,
                Direction.W,
                Direction.NW,
                Direction.NE,
                Direction.E,
            )
        )

        # THEN
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
        res, _ = solve_part1(_parse(raw.splitlines(keepends=True)))

        # THEN
        assert_that(res, equal_to(10))


class TestDoXDailyFlips:
    def test_should_validate_given_example_on_day_1(self):
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
        _, tiles_at_day0 = solve_part1(_parse(raw.splitlines(keepends=True)))

        # WHEN
        tiles = do_x_daily_flips(
            tiles_at_day0,
            number_of_days=1
        )

        # THEN
        assert_that(
            _count_black(tiles),
            equal_to(15)
        )

    def test_should_validate_given_example_on_day_10(self):
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
        _, tiles_at_day0 = solve_part1(_parse(raw.splitlines(keepends=True)))

        # WHEN
        tiles = do_x_daily_flips(
            tiles_at_day0,
            number_of_days=10
        )

        # THEN
        assert_that(
            _count_black(tiles),
            equal_to(37)
        )

    def test_should_validate_given_example_on_day_100(self):
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
        _, tiles_at_day0 = solve_part1(_parse(raw.splitlines(keepends=True)))

        # WHEN
        tiles = do_x_daily_flips(
            tiles_at_day0,
            number_of_days=100
        )

        # THEN
        assert_that(
            _count_black(tiles),
            equal_to(2208)
        )
