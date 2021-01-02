from hamcrest import equal_to, assert_that

from aoc.day13.shuttle_search import _parse, get_best_shuttle, _parse_shuttle_ids, get_earliest_timestamp


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


class TestGetEarliestTimestamp:
    def test_should_validate_first_example(self):
        # GIVEN
        raw = "7,13,x,x,59,x,31,19"

        # WHEN
        timestamp = get_earliest_timestamp(
            _parse_shuttle_ids(raw)
        )

        # THEN
        assert_that(timestamp, equal_to(1068781))

    def test_should_validate_second_example(self):
        # GIVEN
        raw = "17,x,13,19"

        # WHEN
        timestamp = get_earliest_timestamp(
            _parse_shuttle_ids(raw)
        )

        # THEN
        assert_that(timestamp, equal_to(3417))

    def test_should_validate_third_example(self):
        # GIVEN
        raw = "67,7,59,61"

        # WHEN
        timestamp = get_earliest_timestamp(
            _parse_shuttle_ids(raw)
        )

        # THEN
        assert_that(timestamp, equal_to(754018))

    def test_should_validate_fourth_example(self):
        # GIVEN
        raw = "67,x,7,59,61"

        # WHEN
        timestamp = get_earliest_timestamp(
            _parse_shuttle_ids(raw)
        )

        # THEN
        assert_that(timestamp, equal_to(779210))

    def test_should_validate_fifth_example(self):
        # GIVEN
        raw = "67,7,x,59,61"

        # WHEN
        timestamp = get_earliest_timestamp(
            _parse_shuttle_ids(raw)
        )

        # THEN
        assert_that(timestamp, equal_to(1261476))

    def test_should_validate_sixth_example(self):
        # GIVEN
        raw = "1789,37,47,1889"

        # WHEN
        timestamp = get_earliest_timestamp(
            _parse_shuttle_ids(raw)
        )

        # THEN
        assert_that(timestamp, equal_to(1202161486))

    def test_should_validate_basic_example(self):
        # GIVEN
        raw = "2,3,5"

        # WHEN
        timestamp = get_earliest_timestamp(
            _parse_shuttle_ids(raw)
        )

        # THEN
        assert_that(timestamp, equal_to(8))
