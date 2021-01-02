from hamcrest import assert_that, equal_to

from aoc.day12.rain_risk import Position, calculate_manhattan_distance, move, _parse, Direction, move2, _turn2


class TestCalculateManhattanDistance:
    def test_should_calculate_given_example(self):
        # GIVEN
        orig = Position(x=0, y=0)
        dest = Position(x=17, y=-8)

        # WHEN
        distance = calculate_manhattan_distance(orig, dest)

        # THEN
        assert_that(distance, equal_to(25))


class TestMove:
    def test_should_calculate_given_example(self):
        # GIVEN
        raw_lines = """F10
N3
F7
R90
F11"""

        # WHEN
        position = move(
            instructions=_parse(raw_lines.splitlines(keepends=True)),
            position=Position(),
            direction=Direction.EAST
        )

        # THEN
        assert_that(position, equal_to(Position(x=17, y=-8)))


class TestMove2:
    def test_should_calculate_given_example(self):
        # GIVEN
        raw_lines = """F10
N3
F7
R90
F11"""

        # WHEN
        position = move2(
            instructions=_parse(raw_lines.splitlines(keepends=True)),
            position=Position(),
            waypoint=Position(10, 1)
        )

        # THEN
        assert_that(position, equal_to(Position(x=214, y=-72)))


class TestTurn2:
    def test_should_turn_right_by_90(self):
        # GIVEN
        waypoint = Position(3, 5)

        # WHEN
        dest = _turn2(90, waypoint)

        # THEN
        assert_that(dest, equal_to(Position(x=5, y=-3)))

    def test_should_turn_right_by_180(self):
        # GIVEN
        waypoint = Position(3, 5)

        # WHEN
        dest = _turn2(180, waypoint)

        # THEN
        assert_that(dest, equal_to(Position(x=-3, y=-5)))

    def test_should_turn_right_by_270(self):
        # GIVEN
        waypoint = Position(3, 5)

        # WHEN
        dest = _turn2(270, waypoint)

        # THEN
        assert_that(dest, equal_to(Position(x=-5, y=3)))
