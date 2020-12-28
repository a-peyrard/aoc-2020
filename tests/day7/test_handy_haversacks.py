from hamcrest import assert_that, equal_to

from aoc.day7.handy_haversacks import count_bags_containing, _parse


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
            bags=_parse(raw.splitlines(keepends=True)),
            bag_name="shiny gold"
        )

        # THEN
        assert_that(res, equal_to(4))
