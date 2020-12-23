from hamcrest import assert_that, equal_to

from aoc.day2.match_passwords import _parse_raw_password_item, validate_passwords


class TestValidatePasswords:
    def test_should_validate_given_example(self):
        # GIVEN
        # noinspection SpellCheckingInspection
        passwords = list(map(
            _parse_raw_password_item,
            [
                "1-3 a: abcde",
                "1-3 b: cdefg",
                "2-9 c: ccccccccc"
            ]
        ))

        # WHEN
        res = validate_passwords(passwords)

        # THEN
        assert_that(res, equal_to(2))
