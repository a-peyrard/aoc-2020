from hamcrest import assert_that, contains_inanyorder, contains_exactly

from aoc.day22.crab_combat import _parse


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
