import re

from hamcrest import assert_that, equal_to

from aoc.day4.functional import compose
from aoc.day4.validators import number_validator, or_validator, regex_extractor, exists_validator, in_validator, \
    regex_validator


class TestNumberValidator:
    def test_should_validate_number_in_range(self):
        # GIVEN
        val = "123"

        # WHEN
        res = number_validator(min_bound=100, max_bound=200)(val)

        # THEN
        assert_that(res, equal_to(True))

    def test_should_not_validate_number_not_in_range(self):
        # GIVEN
        val = "123"

        # WHEN
        res = number_validator(min_bound=10, max_bound=100)(val)

        # THEN
        assert_that(res, equal_to(False))

    def test_should_not_validate_value_not_being_a_number(self):
        # GIVEN
        val = "abc"

        # WHEN
        res = number_validator(min_bound=10, max_bound=100)(val)

        # THEN
        assert_that(res, equal_to(False))

    def test_should_not_validate_none_value(self):
        # GIVEN
        val = None

        # WHEN
        res = number_validator(min_bound=10, max_bound=100)(val)

        # THEN
        assert_that(res, equal_to(False))


class TestOrValidator:
    def test_should_combine_multiple_validators(self):
        # GIVEN
        val_ok1 = "123"
        val_ok2 = "11"
        val_ko = "110"

        # WHEN
        validator = or_validator([
            number_validator(min_bound=10, max_bound=15),
            number_validator(min_bound=120, max_bound=200)
        ])
        res_ok1 = validator(val_ok1)
        res_ok2 = validator(val_ok2)
        res_ko = validator(val_ko)

        # THEN
        assert_that(res_ok1, equal_to(True))
        assert_that(res_ok2, equal_to(True))
        assert_that(res_ko, equal_to(False))


class TestRegexExtractor:
    def test_should_extract_sub_value(self):
        # GIVEN
        val = "185cm"

        # WHEN
        extracted = regex_extractor(r"^(\d+)cm$")(val)

        # THEN
        assert_that(extracted, equal_to("185"))

    def test_should_return_none_if_no_match(self):
        # GIVEN
        val = "185cm"

        # WHEN
        extracted = regex_extractor(r"^(\d+)in$")(val)

        # THEN
        assert_that(extracted, equal_to(None))


class TestExistsValidator:
    def test_should_validate_if_value_is_not_none(self):
        # GIVEN
        val = "foobar"

        # WHEN
        res = exists_validator()(val)

        # THEN
        assert_that(res, equal_to(True))

    def test_should_not_validate_if_value_is_none(self):
        # GIVEN
        val = None

        # WHEN
        res = exists_validator()(val)

        # THEN
        assert_that(res, equal_to(False))


class TestInValidator:
    def test_should_validate_if_value_is_in_set(self):
        # GIVEN
        val = "foo"
        allowed = {"bar", "foo", "hello"}

        # WHEN
        res = in_validator(allowed)(val)

        # THEN
        assert_that(res, equal_to(True))

    def test_should_not_validate_if_value_is_not_in_set(self):
        # GIVEN
        val = "world"
        allowed = {"bar", "foo", "hello"}

        # WHEN
        res = in_validator(allowed)(val)

        # THEN
        assert_that(res, equal_to(False))


class TestComposedValidators:
    def test_should_validate_simple_regex(self):
        # GIVEN
        validator = compose(exists_validator(), regex_extractor(r"^(\d{9})$"))
        val = "093154719"

        # WHEN
        res = validator(val)

        # THEM
        assert_that(res, equal_to(True))


class TestRegexValidator:
    def test_should_validate_regex(self):
        # GIVEN
        val = "093154719"

        # WHEN
        res = regex_validator(r"\d{9}")(val)

        # THEM
        assert_that(res, equal_to(True))
