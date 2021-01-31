from hamcrest import contains_exactly, assert_that

from aoc.day24.lobby_layout import _parse_directions, Direction, _parse


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


