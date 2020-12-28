from hamcrest import assert_that, equal_to

from aoc.day7.handy_haversacks import count_bags_containing, _parse, count_bags_into


class TestCountBagsContaining:
    def test_should_validate_given_example(self):
        # GIVEN
        raw = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

        # WHEN
        res = count_bags_containing(
            bag_name="shiny gold",
            bags=_parse(raw.splitlines(keepends=True))
        )

        # THEN
        assert_that(res, equal_to(4))


class TestCountBagsInto:
    def test_should_validate_first_example(self):
        # GIVEN
        raw = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

        # WHEN
        res = count_bags_into(
            bag_name="shiny gold",
            bags=_parse(raw.splitlines(keepends=True))
        )

        # THEN
        assert_that(res, equal_to(32))

    def test_should_validate_second_example(self):
        # GIVEN
        raw = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

        # WHEN
        res = count_bags_into(
            bag_name="shiny gold",
            bags=_parse(raw.splitlines(keepends=True))
        )

        # THEN
        assert_that(res, equal_to(126))
