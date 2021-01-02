from hamcrest import equal_to, assert_that

from aoc.day13.shuttle_search import _parse, get_best_shuttle


class TestGetBestShuttle:
    def test_should_validate_given_example(self):
        # GIVEN
        raw = """939
7,13,x,x,59,x,31,19"""

        # WHEN
        shuttle = get_best_shuttle(
            *_parse(raw.splitlines(keepends=True))
        )

        # THEN
        assert_that(shuttle.id * shuttle.waiting_time, equal_to(295))
