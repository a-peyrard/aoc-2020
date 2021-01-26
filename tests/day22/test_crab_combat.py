from collections import deque

from hamcrest import assert_that, contains_exactly, equal_to

from aoc.day22.crab_combat import _parse, play_game, _calculate_score


class TestParse:
    def test_should_parse_players_decks(self):
        # GIVEN
        raw = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

        # WHEN
        deck1, deck2 = _parse(raw.splitlines(keepends=True))

        # THEN
        # noinspection PyTypeChecker
        assert_that(
            deck1,
            contains_exactly(
                9, 2, 6, 3, 1
            )
        )

        # noinspection PyTypeChecker
        assert_that(
            deck2,
            contains_exactly(
                5, 8, 4, 7, 10
            )
        )


class TestPlayGame:
    def test_should_validate_given_example(self):
        # GIVEN
        raw = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

        # WHEN
        score = play_game(*_parse(raw.splitlines(keepends=True)))

        # THEN
        assert_that(score, equal_to(306))


class TestCalculateScore:
    def test_should_calculate_score(self):
        # GIVEN
        deck = deque((3, 2, 10, 6, 8, 5, 9, 4, 7, 1))

        # WHEN
        score = _calculate_score(deck)

        # THEN
        assert_that(score, equal_to(306))
