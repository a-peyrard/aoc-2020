from hamcrest import equal_to, assert_that

from aoc.day25.combo_breaker import _do_loop, _find_loop_size, solve_part1


class TestDoLoop:
    def test_should_generate_given_pub_key(self):
        # GIVEN
        subject = 7

        # WHEN
        pub_key = _do_loop(subject, loop_size=8)

        # THEN
        assert_that(pub_key, equal_to(5764801))

    def test_should_generate_given_door_pub_key(self):
        # GIVEN
        subject = 7

        # WHEN
        pub_key = _do_loop(subject, loop_size=11)

        # THEN
        assert_that(pub_key, equal_to(17807724))

    def test_should_generate_encryption_key_for_given_pub_key(self):
        # GIVEN
        pub_key = 5764801

        # WHEN
        encryption_key = _do_loop(subject=pub_key, loop_size=11)

        # THEN
        assert_that(encryption_key, equal_to(14897079))

    def test_should_generate_encryption_key_for_given_door_pub_key(self):
        # GIVEN
        pub_key = 17807724

        # WHEN
        encryption_key = _do_loop(subject=pub_key, loop_size=8)

        # THEN
        assert_that(encryption_key, equal_to(14897079))


class TestFindLoopSize:
    def test_should_find_loop_size_for_given_pub_key(self):
        # GIVEN
        pub_key = 5764801

        # WHEN
        loop_size = _find_loop_size(subject=7, expected_key=pub_key)

        # THEN
        assert_that(loop_size, equal_to(8))

    def test_should_find_loop_size_for_given_door_pub_key(self):
        # GIVEN
        pub_key = 17807724

        # WHEN
        loop_size = _find_loop_size(subject=7, expected_key=pub_key)

        # THEN
        assert_that(loop_size, equal_to(11))


class TestSolvePart1:
    def test_should_solve_given_example(self):
        # GIVEN
        card_pub_key = 5764801
        door_pub_key = 17807724

        # WHEN
        encryption_key = solve_part1(card_pub_key, door_pub_key)

        # THEN
        assert_that(encryption_key, equal_to(14897079))
