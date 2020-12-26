from hamcrest import assert_that, equal_to

from aoc.day4.passport_processing import count_valid_passports, REQUIRED_PASSPORT_FIELDS


class TestCountValidPassports:

    def test_should_validate_given_example(self):
        # GIVEN
        raw_entries = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

        # WHEN
        res = count_valid_passports(
            raw_entries.splitlines(keepends=True),
            REQUIRED_PASSPORT_FIELDS
        )

        # THEN
        assert_that(res, equal_to(2))
