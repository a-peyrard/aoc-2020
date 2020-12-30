from hamcrest import assert_that, equal_to

from aoc.day10.adapter_array import find_joltage_difference


class TestFindJoltageDifference:
    def test_should_validate_first_example(self):
        # GIVEN
        raw_adapters = """16
10
15
5
1
11
7
19
6
12
4"""

        # WHEN
        res = find_joltage_difference(
            adapters=list(map(int, raw_adapters.splitlines(keepends=True)))
        )

        # THEN
        assert_that(res, equal_to(35))

    def test_should_validate_second_example(self):
        # GIVEN
        raw_adapters = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

        # WHEN
        res = find_joltage_difference(
            adapters=list(map(int, raw_adapters.splitlines(keepends=True)))
        )

        # THEN
        assert_that(res, equal_to(220))
